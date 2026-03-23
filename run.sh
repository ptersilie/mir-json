#!/bin/sh

# Clone a rust repo.
git clone https://github.com/softdevteam/sparsevec/
cd sparsevec

# Create a MIR dump with minimum optimisations enabled.
cargo clean && cargo +nightly rustc -- -C opt-level=0 -Z mir-opt-level=0 -Zdump-mir=all
mv mir_dump noopt_mir
python ../mir-to-json.py noopt_mir
rm noopt_mir/*.mir
rm noopt_mir/*.dot

# Create MIR dumps with selected optimisations enabled:
passes=("RemoveUnneededDrops" "SingleUseConsts" "CopyProp" "SimplifyLocals-after-value-numbering")
for pass in "${passes[@]}"; do
    folder="${pass}_mir"
    cargo clean && cargo +nightly rustc -- -C opt-level=0 -Z mir-opt-level=0 -Z mir-enable-passes=+$pass -Zdump-mir=all
    mv mir_dump $folder
    python ../mir-to-json.py $folder
    rm $folder/*.mir
    rm $folder/*.dot
done

# Create a MIR dump with default optimisations enabled.
cargo clean && cargo +nightly rustc -- -Zdump-mir=all
mv mir_dump opt_mir
python ../mir-to-json.py opt_mir
rm opt_mir/*.mir
rm opt_mir/*.dot
