#!/usr/bin/env bash
set -eu
R="$PWD"
export XDG_CONFIG_HOME="$R/.cache/orca/config"
export XDG_CACHE_HOME="$R/.cache/orca/cache"
export XDG_RUNTIME_DIR="$(mktemp -d "$HOME/.cache/orca-native.XXXXXX")"
export NO_AT_BRIDGE=0
export GTK_A11Y=always
export PLAYWRIGHT_BROWSERS_PATH="/home/user/.cache/ms-playwright"
export ACCESSIBILITY_ENABLED=1
export MOZ_ACCESSIBILITY_ATSPI=1
mkdir -p "$XDG_CONFIG_HOME" "$XDG_CACHE_HOME" "$XDG_RUNTIME_DIR"
chmod 700 "$XDG_RUNTIME_DIR"
openbox > .cache/orca/openbox.log 2>&1 &
wm=$!
export PULSE_SERVER="unix:$XDG_RUNTIME_DIR/orca-pulse.sock"
cat > .cache/orca/pulse-minimal.pa <<EOF
load-module module-native-protocol-unix socket=$XDG_RUNTIME_DIR/orca-pulse.sock auth-anonymous=1
load-module module-null-sink sink_name=orca_review sink_properties=device.description=OrcaReview
set-default-sink orca_review
EOF
pulseaudio --daemonize=no --use-pid-file=no --realtime=no --high-priority=no --exit-idle-time=-1 --disable-shm=yes -n -F "$R/.cache/orca/pulse-minimal.pa" --log-target=file:"$R/.cache/orca/pulse.log" > .cache/orca/pulse-console.log 2>&1 &
pa=$!
python3 - <<'READY'
import os,socket,time
path=os.environ['XDG_RUNTIME_DIR']+'/orca-pulse.sock'
for _ in range(50):
 try:
  s=socket.socket(socket.AF_UNIX);s.connect(path);s.close();break
 except OSError:time.sleep(.1)
else:raise RuntimeError('PulseAudio fixture socket did not start')
READY
pactl info > .cache/orca/pulse-info.txt
parec --device=orca_review.monitor --format=s16le --rate=16000 --channels=1 > .cache/orca/speech.raw &
rec=$!
gsettings set org.gnome.desktop.a11y.applications screen-reader-enabled true
mkdir -p .cache/orca/speech-config
cat > .cache/orca/speech-config/speechd.conf <<EOF
LogLevel 3
AudioOutputMethod "pulse"
AddModule "espeak-ng" "sd_espeak-ng" "/etc/speech-dispatcher/modules/espeak-ng.conf"
DefaultModule "espeak-ng"
DefaultLanguage "en"
EOF
export SPEECHD_ADDRESS="unix_socket:$XDG_RUNTIME_DIR/speechd.sock"
speech-dispatcher -s -C "$R/.cache/orca/speech-config" -L "$R/.cache/orca/speech-logs" -S "$XDG_RUNTIME_DIR/speechd.sock" -P "$XDG_RUNTIME_DIR/speechd.pid" -t 0 > .cache/orca/speechd.log 2>&1 &
sd=$!
python3 - <<'SDREADY'
import os,time
for _ in range(60):
 if os.path.exists(os.environ['XDG_RUNTIME_DIR']+'/speechd.sock'):break
 time.sleep(.1)
else:raise RuntimeError('Private Speech Dispatcher did not start')
SDREADY
/usr/bin/orca --replace --user-prefs "$R/.cache/orca/prefs" --enable speech --disable braille --debug-file "$R/.cache/orca/orca-debug.log" > .cache/orca/orca-console.log 2>&1 &
at=$!
cleanup(){ kill "$rec" "$at" "$wm" "$sd" "$pa" 2>/dev/null || true; }
trap cleanup EXIT
python3 .cache/orca/drive.py
