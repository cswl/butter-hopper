#!/bin/bash


btr_path="$1" 
btrfs filesystem df "$btr_path"
