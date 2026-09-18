if [ "$LD_LIBRARY_PATH" == "$P2_LIB_B" ]; then
    export LD_LIBRARY_PATH="$P2_LIB_A"
fi
$P2_APP