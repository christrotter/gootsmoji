# gootsmoji
Collection of very useful slack emojis.

## Preview 
![Goots goots goots](grid_image.png?raw=true)

## Gootsifying your Slack workspace

You can sync available Goots at any time by running the bootstrap script (`. script/bootstrap`) and running the
`import.py` script. Note that this requires a valid configuration file to be present.

```bash
python ./import.py <path-to-goots-config-json>
```

### Configuration

The importer ("Goots Cannon") relies on the same APIs the app uses to avoid limitations due to Slack Enterprise. Because
of this, you will need to supply two authentication tokens that you can retrieve by logging in via Slack web and inspecting your local storage and cookies.

The first token, `xoxc`, is available under your browser's Local Storage if you look up the value of
`localConfig_v2.teams.[team_id].token` and is of the form `xoxc-*`.

The second token, `xoxd` is stored in a cookie named `d` attached to your Slack web session and is of the form `xoxd-*`.

With those two tokens in hand, you can build a valid configuration file:

```json
{
   "xoxc": "xoxc-...",
   "xoxd": "xoxd-...",
   "api_host": "my-slack-workspace.slack.com",
}
```

Optionally, you can include a `assets_root` value which overrides the default for where the tool should find the goots
(by default, `./goots`, where the PNGs live). You can also tweak the number of retries allowed in the event of rate
limiting by defining `max_retries` (defaults to 5).
