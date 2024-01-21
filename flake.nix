{
  description = "Gemini Cli";

  inputs = {
    flake-utils.url = "github:numtide/flake-utils";
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    poetry2nix = {
      url = "github:nix-community/poetry2nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = { self, nixpkgs, flake-utils, poetry2nix }:
  flake-utils.lib.eachDefaultSystem (system:
  let
    # see https://github.com/nix-community/poetry2nix/tree/master#api for more functions and examples.
    pkgs = nixpkgs.legacyPackages.${system};
    p2n = poetry2nix.lib.mkPoetry2Nix { inherit pkgs; };
    inherit (p2n) mkPoetryApplication;
  in
  {
    packages = {
      gemini-cli = mkPoetryApplication { 
        projectDir = self;
        overrides = p2n.defaultPoetryOverrides.extend
        (self: super: {
          inherit (pkgs.python311Packages) grpcio;
          inherit (pkgs.python311Packages) grpcio-status;
          inherit (pkgs.python311Packages)  googleapis-common-protos;
          inherit (pkgs.python311Packages) protobuf;

          google-ai-generativelanguage = super.google-ai-generativelanguage.overridePythonAttrs
          (
            old: {
              buildInputs = (old.buildInputs or [ ]) ++ [ super.setuptools ];
            }
            );
          });
        };
        default = self.packages.${system}.gemini-cli;
      };

      devShells.default = pkgs.mkShell {
        inputsFrom = [ self.packages.${system}.gemini-cli];
        packages = [ pkgs.poetry ];
      };
    });
  }
