<script lang="ts">
  import { onMount } from 'svelte';

  let intelFeed = []; // This will hold our data
  let isLoading = true;

  // This function runs automatically when the component loads
  onMount(async () => {
    try {
      // This is your Command Center talking to your Bunker
      const response = await fetch('https://271triliun.xyz/api/get_whale_data.php'); // <-- REPLACE THIS URL
      if (!response.ok) {
        throw new Error(`Bunker Network Error: ${response.status}`);
      }
      intelFeed = await response.json();
    } catch (error) {
      console.error("Failed to retrieve intelligence:", error);
    } finally {
      isLoading = false;
    }
  });
</script>

<main class="bg-black text-green-400 font-mono p-4 min-h-screen">
  <h1 class="text-3xl border-b border-red-700 pb-2 mb-4 animate-pulse">COMMAND CENTER // SIGINT_FEED</h1>
  
  <div class="border border-green-800 p-2">
    <h2 class="text-xl text-yellow-400 mb-2">[WHALER MOVEMENTS // REAL-TIME]</h2>
    
    {#if isLoading}
      <p class="animate-ping">...CONTACTING BUNKER...</p>
    {:else if intelFeed.length === 0}
      <p class="text-red-500"> NO INTEL AVAILABLE. FEED IS COLD. </p>
    {:else}
      <div class="overflow-x-auto">
        <table class="w-full text-left">
          <thead class="border-b border-green-700 text-yellow-400">
            <tr>
              <th class="p-1">TIMESTAMP</th>
              <th class="p-1">LABEL</th>
              <th class="p-1">WALLET</th>
              <th class="p-1">ACTION</th>
            </tr>
          </thead>
          <tbody>
            {#each intelFeed as entry}
              <tr class="border-b border-green-900 hover:bg-green-900/50">
                <td class="p-1 whitespace-nowrap">{entry.timestamp}</td>
                <td class="p-1 text-red-500">{entry.wallet_label}</td>
                <td class="p-1">{entry.wallet_address.substring(0, 10)}...</td>
                <td class="p-1 text-white">{entry.action}</td>
              </tr>
            {/each}
          </tbody>
        </table>
      </div>
    {/if}
  </div>
</main>