{pkgs,  poetry2nix} : poetry2nix.mkPoetryApplication { 
  projectDir = ./.;
  python = pkgs.python311;
  overrides = poetry2nix.defaultPoetryOverrides.extend (self: 
  super: {
    inherit (pkgs.python311Packages) grpcio;
    inherit (pkgs.python311Packages) grpcio-status;
    inherit (pkgs.python311Packages) googleapis-common-protos;
    inherit (pkgs.python311Packages) protobuf;

    google-ai-generativelanguage = super.google-ai-generativelanguage.overridePythonAttrs (
      old: {
        buildInputs = (old.buildInputs or [ ]) ++ [ super.setuptools ];
      }
      );
    }
    );
  }
