#!/bin/bash
nix-shell --run "firebase emulators:start --only auth,firestore"
