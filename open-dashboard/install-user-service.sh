cp chromium-kiosk.service ~/.config/systemd/user/chromium-kiosk.service
systemctl --user daemon-reload
systemctl --user enable --now chromium-kiosk.service
loginctl enable-linger $USER
