#!/bin/zsh

readonly SCHEME_DIR=$HOME/.config/colorschemes
active=$(cat $SCHEME_DIR/active)
echo "Setting $active"
readonly ACTIVE_SCHEME=$SCHEME_DIR/$active
readonly XFCE4_TERMRC=$HOME/.config/xfce4/terminal/terminalrc
readonly XRES=$HOME/.Xresources
readonly I3_SCRIPTS=$HOME/.config/i3blocks/scripts/
readonly I3_CONF=$HOME/.config/i3/config

get_hex () {
    echo $( grep "$1" $ACTIVE_SCHEME | grep -m 1 -Po "#\w{6}$" )
}

append_xfce4 () {
    echo $1 >> $XFCE4_TERMRC
}

append_xres() {
    echo $1 >> $XRES
}

readonly FOREGROUND=$( get_hex "foreground" )
readonly BACKGROUND=$( get_hex "background" )
readonly COLOR0=$( get_hex "color0" )
readonly COLOR1=$( get_hex "color1" )
readonly COLOR2=$( get_hex "color2" )
readonly COLOR3=$( get_hex "color3" )
readonly COLOR4=$( get_hex "color4" )
readonly COLOR5=$( get_hex "color5" )
readonly COLOR6=$( get_hex "color6" )
readonly COLOR7=$( get_hex "color7" )
readonly COLOR8=$( get_hex "color8" )
readonly COLOR9=$( get_hex "color9" )
readonly COLOR10=$( get_hex "color10" )
readonly COLOR11=$( get_hex "color11" )
readonly COLOR12=$( get_hex "color12" )
readonly COLOR13=$( get_hex "color13" )
readonly COLOR14=$( get_hex "color14" )
readonly COLOR15=$( get_hex "color15" )
readonly TOP0=$( get_hex "top0" )
readonly TOP1=$( get_hex "top1" )
readonly TOP2=$( get_hex "top2" )
readonly TOP3=$( get_hex "top3" )
readonly OPP0=$( get_hex "opp0" )
readonly OPP1=$( get_hex "opp1" )
readonly OPP2=$( get_hex "opp2" )
readonly OPP3=$( get_hex "opp3" )

# writes xfce4-terminal color palette
readonly XFCE_COLOR="$COLOR0;$COLOR1;$COLOR2;$COLOR3;$COLOR4;$COLOR5;$COLOR6;$COLOR7;$COLOR8;$COLOR9;$COLOR10;$COLOR11;$COLOR12;$COLOR13;$COLOR14;$COLOR15"
cat $HOME/.config/xfce4/terminal/terminalrc.static > $XFCE4_TERMRC
append_xfce4 "ColorBackground=$BACKGROUND"
append_xfce4 "ColorForeground=$FOREGROUND"
append_xfce4 "ColorCursor=$TOP1"
append_xfce4 "ColorPalette=$XFCE_COLOR"


# writex rofi colors
cat $HOME/.Xresources.static > $XRES
rofi_win="rofi.color-window: $BACKGROUND, $BACKGROUND, $BACKGROUND"
rofi_norm="rofi.color-normal: $BACKGROUND, $FOREGROUND, $BACKGROUND, $TOP0, $OPP0"
rofi_act="rofi.color-active: $BACKGROUND, $FOREGROUND, $BACKGROUND, $TOP1, $OPP1"
rofi_urg="rofi.color-urgent: $BACKGROUND, $FOREGROUND, $BACKGROUND, $TOP3, $OPP3"
append_xres "! State:           bg       border   split"
append_xres "$rofi_win"
append_xres "! State:           bg       fg       bgalt    hlbg     hlgf"
append_xres "$rofi_norm"
append_xres "$rofi_act"
append_xres "$rofi_urg"

# writes colors so i3bar scripts can use them
readonly HEADER='#!/bin/zsh'
# power
echo "$HEADER" > $I3_SCRIPTS/power.color
echo "readonly BG='$BACKGROUND'" >> $I3_SCRIPTS/power.color
echo "readonly TOP0='$TOP0'" >> $I3_SCRIPTS/power.color
echo "readonly TOP3='$TOP3'" >> $I3_SCRIPTS/power.color
echo "readonly OPP0='$OPP0'" >> $I3_SCRIPTS/power.color
echo "readonly OPP3='$OPP3'" >> $I3_SCRIPTS/power.color
cat $I3_SCRIPTS/power.static >> $I3_SCRIPTS/power.color
# volume
echo "$HEADER" > $I3_SCRIPTS/volume.color
echo "readonly BG='$BACKGROUND'" >> $I3_SCRIPTS/volume.color
echo "readonly OPP3='$OPP3'" >> $I3_SCRIPTS/volume.color
cat $I3_SCRIPTS/volume.static >> $I3_SCRIPTS/volume.color
# cpu-load
echo "$HEADER" > $I3_SCRIPTS/cpu-load.color
echo "readonly BG='$BACKGROUND'" >> $I3_SCRIPTS/cpu-load.color
echo "readonly TOP3='$TOP3'" >> $I3_SCRIPTS/cpu-load.color
echo "readonly OPP3='$OPP3'" >> $I3_SCRIPTS/cpu-load.color
cat $I3_SCRIPTS/cpu-load.static >> $I3_SCRIPTS/cpu-load.color
# mem-usage
echo "$HEADER" > $I3_SCRIPTS/mem-usage.color
echo "readonly BG='$BACKGROUND'" >> $I3_SCRIPTS/mem-usage.color
echo "readonly TOP3='$TOP3'" >> $I3_SCRIPTS/mem-usage.color
echo "readonly OPP3='$OPP3'" >> $I3_SCRIPTS/mem-usage.color
cat $I3_SCRIPTS/mem-usage.static >> $I3_SCRIPTS/mem-usage.color
# mpdtest
echo "$HEADER" > $I3_SCRIPTS/mpdtest.color
echo "readonly BG='$BACKGROUND'" >> $I3_SCRIPTS/mpdtest.color
echo "readonly OPP3='$OPP3'" >> $I3_SCRIPTS/mpdtest.color
cat $I3_SCRIPTS/mpdtest.static >> $I3_SCRIPTS/mpdtest.color
# make all executable
chmod 755 $I3_SCRIPTS/*.color

# writes colors to i3 config
echo 'set $background ' "$BACKGROUND" > $I3_CONF
echo 'set $foreground ' "$FOREGROUND" >> $I3_CONF
echo 'set $gray ' "$COLOR8" >> $I3_CONF
echo 'set $top0 ' "$TOP0" >> $I3_CONF
echo 'set $top1 ' "$TOP1" >> $I3_CONF
echo 'set $top2 ' "$TOP2" >> $I3_CONF
echo 'set $top3 ' "$TOP3" >> $I3_CONF
echo 'set $opp0 ' "$OPP0" >> $I3_CONF
echo 'set $opp1 ' "$OPP1" >> $I3_CONF
echo 'set $opp2 ' "$OPP2" >> $I3_CONF
echo 'set $opp3 ' "$OPP3" >> $I3_CONF
cat $I3_CONF.static >> $I3_CONF

# reload Xresources & restart i3
xrdb $XRES
i3-msg restart
