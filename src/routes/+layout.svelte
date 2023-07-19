<script>
  import '../app.css';
</script>

<svelte:head>
  <title>Land Value PH</title>
  <meta
    name="description"
    content="landvalue.ph : interactive map of property values in Greater Metro Manila area Philippines" />
  <link
    rel="icon"
    href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>🗺️</text></svg>" />
</svelte:head>

<main class="h-screen min-h-screen">
  <slot />
</main>
