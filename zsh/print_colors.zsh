#!/bin/zsh

for i in 0 1
do
    echo -n "\e[$i$(echo 'm')    $i\e[0m "
    for k in {40..47}
    do
        echo -n "\e[$i;$k$(echo 'm')    $i;$k\e[0m "
    done
    echo -n "\n"
    for j in {30..37}
    do
        echo -n "\e[$i;$j$( echo 'm' ) $i;$j\e[0m "
        for k in {40..47}
        do
            echo -n "\e[$i;$j;$k$( echo 'm') $i;$j;$k\e[0m "
        done
        echo -n "\n"
    done
done

echo "\e[0m"
