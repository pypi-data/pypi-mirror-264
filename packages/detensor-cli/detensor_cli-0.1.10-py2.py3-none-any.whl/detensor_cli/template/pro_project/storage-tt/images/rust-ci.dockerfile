FROM rust:latest

COPY rust-cargo-config.toml /usr/local/cargo/config

RUN ["rustup", "target", "add", "wasm32-unknown-unknown"]
RUN ["rustup", "component", "add", "clippy"]
RUN ["cargo", "install", "cargo-sort"]
RUN ["rustup", "toolchain", "add", "nightly"]
RUN ["rustup", "component", "add", "rustfmt", "--toolchain", "nightly-x86_64-unknown-linux-gnu"]
