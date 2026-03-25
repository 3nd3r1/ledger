{
  pkgs ? import <nixpkgs> { },
}:

pkgs.mkShell {
  buildInputs = with pkgs; [
    python311

    stdenv.cc.cc.lib
    zlib
    libffi
    openssl
  ];

  shellHook = ''
    export LD_LIBRARY_PATH="${pkgs.stdenv.cc.cc.lib}/lib:${pkgs.zlib}/lib:$LD_LIBRARY_PATH"
    if [ ! -d venv ]; then
      python -m venv venv
	  pip install --upgrade pip
      pip install -q -r requirements-dev.txt
    fi
    source venv/bin/activate
  '';
}
