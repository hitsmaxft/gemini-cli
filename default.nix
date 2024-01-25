{ pkgs, poetry2nix }: poetry2nix.mkPoetryApplication {
  projectDir = ./.;
  python = pkgs.python311;
  overrides = poetry2nix.defaultPoetryOverrides.extend (self:
    super: {
      inherit (pkgs.python311Packages) googleapis-common-protos;
      inherit (pkgs.python311Packages) 
      cachetools             
      certifi                      
      charset-normalizer           
      grpcio                       
      grpcio-status                
      idna                         
      proto-plus                   
      protobuf                     
      pyasn1                       
      pyasn1-modules               
      requests                     
      rsa                          
      toml                         
      tqdm                         
      typing-extensions            
      rich 
      urllib3;

      google-ai-generativelanguage = super.google-ai-generativelanguage.overridePythonAttrs (
        old: {
          buildInputs = (old.buildInputs or [ ]) ++ [ super.setuptools ];
        }
      );
    }
  );
}
