// Mermaid vestido com a paleta modus-vivendi (mesmos valores de
// theme/modus-vivendi.css). O livro usa o tema "coal" fixo, então a
// inicialização é única, sem alternância clara/escura.
mermaid.initialize({
  startOnLoad: true,
  theme: 'base',
  themeVariables: {
    darkMode: true,
    background: '#000000',
    fontFamily: '"Open Sans", sans-serif',

    primaryColor: '#2f0c3f',        // bg-magenta-nuanced: preenchimento dos nós
    primaryTextColor: '#ffffff',    // fg-main
    primaryBorderColor: '#b6a0ff',  // magenta-cooler: borda dos nós

    secondaryColor: '#042837',      // bg-cyan-nuanced
    secondaryBorderColor: '#00d3d0',// cyan
    secondaryTextColor: '#ffffff',

    tertiaryColor: '#1e1e1e',       // bg-dim
    tertiaryBorderColor: '#646464', // border
    tertiaryTextColor: '#ffffff',

    lineColor: '#989898',           // fg-dim: setas
    textColor: '#ffffff',
    edgeLabelBackground: '#1e1e1e',

    clusterBkg: '#1e1e1e',
    clusterBorder: '#646464',

    noteBkgColor: '#381d0f',        // bg-yellow-nuanced
    noteTextColor: '#ffffff',
    noteBorderColor: '#fec43f'      // yellow-warmer
  }
});
