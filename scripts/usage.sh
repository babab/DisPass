#!/bin/sh

commands="
    add
    generate
    gui
    list
    rm
    version
"

dispass help



for cmd in ${commands}; do
    echo dispass ${cmd}
    echo ----------------
    echo
    dispass help ${cmd}
    echo
done
