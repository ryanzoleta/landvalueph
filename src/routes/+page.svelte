<script lang="ts">
  import { formatCurrency } from '$lib/utils.js';
  import { onMount } from 'svelte';

  export let data;

  let localityLevel: 'city' | 'district' = 'district';
  let locality = '';

  function getBarangayLocalityId(datasetFeature: any) {
    let localityId = '';

    if (
      datasetFeature.datasetAttributes['ADM2_EN'] ===
      'NCR, CITY OF MANILA, FIRST DISTRICT (Not a Province)'
    ) {
      localityId = datasetFeature.datasetAttributes['ADM3_PCODE'];
    } else {
      localityId = datasetFeature.datasetAttributes['ADM4_PCODE'];
    }

    return localityId;
  }

  function setStyle(params: any) {
    const datasetFeature = params.feature;

    if (localityLevel === 'city') {
      const adminLevel2 = datasetFeature.datasetAttributes['ADM2_EN'];

      let value: string;

      if (adminLevel2 === 'NCR, CITY OF MANILA, FIRST DISTRICT (Not a Province)') {
        value = data.cities['CITY OF MANILA'].color;
      } else {
        const city = datasetFeature.datasetAttributes['ADM3_EN'] as string;
        value = data.cities[city].color;
      }

      return {
        strokeWeight: 3.0,
        fillColor: value,
        fillOpacity: 0.3
      };
    } else if (localityLevel === 'district') {
      try {
        let localityId = getBarangayLocalityId(datasetFeature);

        return {
          strokeColor: locality === localityId ? 'black' : undefined,
          strokeWeight: 3.0,
          fillColor: data.barangays[localityId].color,
          fillOpacity: 0.3
        };
      } catch {
        return {
          strokeWeight: 1.0,
          fillColor: 'gray',
          fillOpacity: 0.3
        };
      }
    }
  }

  function buildPopupElement(name: string, value: number) {
    const element = document.createElement('div');
    element.className = 'bg-zinc-900 p-2 rounded-lg font-bold text-white text-center';

    let innerHTML = `<h1 class="text-md">${name}</h1>`;

    if (value) {
      innerHTML += `<p class="text-lg font-extrabold">${formatCurrency(
        value
      )} <span class="text-xs">per sqm</span></p>`;
    }

    element.innerHTML = innerHTML;

    return element;
  }

  onMount(async () => {
    //@ts-ignore
    let map: google.maps.MapsLibrary;
    let allMarkers: any[] = [];

    async function handleClick(e) {
      //@ts-ignore
      const { AdvancedMarkerElement } = (await google.maps.importLibrary(
        'marker'
        //@ts-ignore
      )) as google.maps.MarkerLibrary;
      const datasetFeature = e.features[0];
      let localityId = getBarangayLocalityId(datasetFeature);

      for (let i = 0; i < allMarkers.length; i++) {
        allMarkers[i].setMap(null);
      }

      const marker = new AdvancedMarkerElement({
        map,
        position: data.barangays[localityId].position,
        content: buildPopupElement(
          data.barangays[localityId].name,
          data.barangays[localityId].value
        )
      });

      allMarkers.push(marker);

      const datasetLayer = map.getDatasetFeatureLayer(data.BARANGAYS_DATASET_ID);
      locality = localityId;
      datasetLayer.style = setStyle;
    }

    //@ts-ignore
    const { Map } = (await google.maps.importLibrary('maps')) as google.maps.MapsLibrary;

    map = new Map(document.getElementById('map') as HTMLElement, {
      center: { lat: 14.5964947, lng: 120.9883602 },
      zoom: 12,
      maxZoom: 15,
      minZoom: 11,
      mapId: data.MAP_ID,
      mapTypeControl: false,
      disableDefaultUI: true
    });

    const datasetLayer = map.getDatasetFeatureLayer(data.BARANGAYS_DATASET_ID);
    datasetLayer.style = setStyle;
    datasetLayer.addListener('click', handleClick);
  });
</script>

<div class="flex h-full flex-col bg-zinc-900">
  <script
    async
    src={`https://maps.googleapis.com/maps/api/js?key=${data.MAPS_API_KEY}&callback=initMap&v=beta`}></script>
  <div class="flex">
    <h1 class="text-white">landvalue.ph</h1>
    <div>
      <select name="viewing" id="inputViewing" bind:value={localityLevel}>
        <option value="city">City</option>
        <option value="district">District</option>
      </select>
    </div>
  </div>
  <div id="map" class="h-full" />
</div>
