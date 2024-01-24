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
        name = "gemini-cli";
      in
      {
        packages.default = pkgs.callPackage ./default.nix {
          poetry2nix = poetry2nix.lib.mkPoetry2Nix { inherit pkgs; };
        };

        formatter = pkgs.nixpkgs-fmt;
        devShells.default = pkgs.mkShell {
          #inputsFrom = [ self.packages.${system}.${name} ];
          packages = [ pkgs.poetry pkgs.python311 ];
          buildInputs = with pkgs; [];
          LD_LIBRARY_PATH="${pkgs.stdenv.cc.cc.lib}/lib/:/run/opengl-driver/lib/";
          shellHook = ''
          '';
        };
        
      });
}
