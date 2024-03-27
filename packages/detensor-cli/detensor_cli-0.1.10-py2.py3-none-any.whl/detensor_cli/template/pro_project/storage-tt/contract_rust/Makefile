build:
	- cargo build --release --target=wasm32-unknown-unknown --lib

pre-format:
	@rustup component add rustfmt
	@cargo install -q cargo-sort

format: pre-format
	@cargo +nightly fmt
	@cargo sort -w ./Cargo.toml > /dev/null

ci-format:
	@cargo +nightly fmt
	@cargo sort -w ./Cargo.toml > /dev/null

clippy:
	cargo clippy --all-targets --all-features --workspace -- -D "warnings"

dev: format clippy

clean:
	cargo clean

.PHONY: build pre-format format ci-format clippy dev clean
