if status is-interactive
    # Commands to run in interactive sessions can go here
    # nitch
end

set -l teal 94e2d5
set -l flamingo f2cdcd
set -l mauve cba6f7
set -l pink f5c2e7
set -l red f38ba8
set -l peach fab387
set -l green a6e3a1
set -l yellow f9e2af
set -l blue 89b4fa
set -l gray 1f1d2e
set -l black 191724

# Completion Pager Colors
set -g fish_pager_color_progress $gray
set -g fish_pager_color_prefix $mauve
set -g fish_pager_color_completion $peach
set -g fish_pager_color_description $gray

set -g man_blink -o $teal
set -g man_bold -o $pink
set -g man_standout -b $gray
set -g man_underline -u $blue

abbr -a -g h 'history'	
abbr -a -g please 'sudo'
abbr -a -g fucking 'sudo'
abbr -a -g shutup 'shutdown now'
abbr -a -g untar 'tar -xzvf'
# Bachelor Thesis modes
abbr -a -g bamode 'conda activate ba'
abbr -a -g badone 'conda deactivate'
abbr -a --position anywhere .c '~/.config/'

# Make su launch fish
function su
    command su --shell=/usr/bin/fish $argv
end

# Make su launch fish
function su
    command su --shell=/usr/bin/fish $argv
end

set MOZ_ENABLE_WAYLAND 1
set EDITOR nvim

# >>> conda initialize >>>
# !! Contents within this block are managed by 'conda init' !!
if test -f /home/beni/.local/bin/miniconda3/bin/conda
    eval /home/beni/.local/bin/miniconda3/bin/conda "shell.fish" "hook" $argv | source
end
# Deactivate Conda base environment
conda deactivate
# <<< conda initialize <<<

fish_add_path /home/beni/.local/bin/spicetify
