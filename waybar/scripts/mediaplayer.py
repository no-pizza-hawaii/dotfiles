#!/usr/bin/env python3
import argparse
import logging
import sys
import signal
import gi
import json
gi.require_version('Playerctl', '2.0')
from gi.repository import Playerctl, GLib

logger = logging.getLogger(__name__)

def getIcon(name):
    icons = {"spotify": " ", "spotify_player": " ", "firefox": " "}
    if name in icons:
        return icons[name]
    else:
        return ""


def write_output(text, player, manager):
    logger.info('Writing output')

    tooltip = ""
    for p in manager.props.players:
        name = p.props.player_name
        tooltip += "\n" + getIcon(name) + name + ":\n"
        tooltip += get_metadata(p, p.props.metadata, manager) + "\n"

    output = {'text': text,
              'tooltip': tooltip,
              'class': 'custom-' + player.props.player_name,
              'alt': player.props.player_name}

    sys.stdout.write(json.dumps(output) + '\n')
    sys.stdout.flush()

def write_metadata(manager):
    logger.info('Writing metadata')

    info = []
    for p in manager.props.players:
        name = p.props.player_name
        # info.append(name)
        info.append(f"[{getIcon(name)} <i>{name}</i>] {get_metadata(p, p.props.metadata, manager)}")
    
    sys.stdout.write('\n'.join(info))
    sys.stdout.flush()

def get_metadata(player, metadata, manager):
    track_info = ''

    if player.props.player_name == 'spotify' and \
            'mpris:trackid' in metadata.keys() and \
            ':ad:' in player.props.metadata['mpris:trackid']:
        track_info = 'AD PLAYING'
    elif player.get_artist() != '' and player.get_title() != '':
        track_info = '{artist} - {title}'.format(artist=player.get_artist(),
                                                 title=player.get_title())
    else:
        track_info = player.get_title()

    if player.props.status != 'Playing' and track_info:
        track_info = ' ' + track_info
    
    return track_info

def on_play(player, status, manager):
    logger.info('Received new playback status')
    on_metadata(player, player.props.metadata, manager)

def on_metadata(player, metadata, manager):
    logger.info('Received new metadata')
    write_output(get_metadata(player, metadata, manager), player, manager)


def on_player_appeared(manager, player, selected_player=None):
    if player is not None and (selected_player is None or player.name == selected_player):
        init_player(manager, player)
    else:
        logger.debug("New player appeared, but it's not the selected player, skipping")


def on_player_vanished(manager, player):
    logger.info('Player has vanished')
    if len(manager.props.players) == 0:
        sys.stdout.write('\n')
    else:
        p = manager.props.players[0]
        on_metadata(p, p.props.metadata, manager)
    sys.stdout.flush()


def init_player(manager, name):
    logger.debug('Initialize player: {player}'.format(player=name.name))
    player = Playerctl.Player.new_from_name(name)
    player.connect('playback-status', on_play, manager)
    player.connect('metadata', on_metadata, manager)
    manager.manage_player(player)
    on_metadata(player, player.props.metadata, manager)


def signal_handler(sig, frame):
    logger.debug('Received signal to stop, exiting')
    sys.stdout.write('\n')
    sys.stdout.flush()
    # loop.quit()
    sys.exit(0)


def parse_arguments():
    parser = argparse.ArgumentParser()

    # Increase verbosity with every occurrence of -v
    parser.add_argument('-v', '--verbose', action='count', default=0)

    # Define for which player we're listening
    parser.add_argument('--player')

    parser.add_argument('--metadata', action='store_true')

    return parser.parse_args()


def main():
    arguments = parse_arguments()

    # Initialize logging
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG,
                        format='%(name)s %(levelname)s %(message)s')

    # Logging is set by default to WARN and higher.
    # With every occurrence of -v it's lowered by one
    logger.setLevel(max((3 - arguments.verbose) * 10, 0))

    # Log the sent command line arguments
    logger.debug('Arguments received {}'.format(vars(arguments)))

    manager = Playerctl.PlayerManager()

    if arguments.metadata:
        for name in manager.props.player_names:
            player = Playerctl.Player.new_from_name(name)
            manager.manage_player(player)
        write_metadata(manager)
        return

    manager.connect('name-appeared', lambda *args: on_player_appeared(*args, arguments.player))
    manager.connect('player-vanished', on_player_vanished)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)

    for player in manager.props.player_names:
        if arguments.player is not None and arguments.player != player.name:
            logger.debug('{player} is not the filtered player, skipping it'
                         .format(player=player.name)
                         )
            continue

        init_player(manager, player)

    loop = GLib.MainLoop()
    loop.run()


if __name__ == '__main__':
    main()
