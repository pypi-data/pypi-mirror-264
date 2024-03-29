# tat_cli
A command-line tool to colorize terminal output with regex. 

Each group in the regex will be colored independently. `tat-cli` supports nested groups and 24-bit colors.

Example usage:

```sh
$ echo "start [121 45567 345] - [454 45563 676] end" | tat "(\[(\d(\d\d)) (\d(\d(\d)\d)\d) ((\d\d)\d)\])"
```
or to specify your own colors or color-pairs:

```sh
$ echo "start [121 45567 345] - [454 45563 676] end" | tat "(\[(\d(\d\d)) (\d(\d(\d)\d)\d) ((\d\d)\d)\])" ff0000 00ff00:ff00ff 0000ff ffff00:0000ff 00ffff ff00ff:00ff00 000000 ffffff:000000
```


How it looks:

![Preview](https://raw.githubusercontent.com/salt-die/tat_cli/main/preview.png)
