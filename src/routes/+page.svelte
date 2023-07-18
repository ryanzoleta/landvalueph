<script lang="ts">
  import { formatCurrency } from '$lib/utils.js';
  import { Loader } from '@googlemaps/js-api-loader';
  import { onMount } from 'svelte';

  let currentLevel: 'city' | 'district' = 'district';
  let selectedLocality = '';

  export let data;

  onMount(() => {
    //@ts-ignore
    let map: google.maps.MapsLibrary;
    let allMarkers: any[] = [];

    const loader = new Loader({
      apiKey: data.MAPS_API_KEY,
      version: 'beta'
    });

    function setStyle(params: any) {
      const datasetFeature = params.feature;

      if (currentLevel === 'city') {
        const adminLevel2 = datasetFeature.datasetAttributes['ADM2_EN'];

        let value;

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
      } else if (currentLevel === 'district') {
        let localityId = '';

        try {
          if (
            datasetFeature.datasetAttributes['ADM2_EN'] ===
            'NCR, CITY OF MANILA, FIRST DISTRICT (Not a Province)'
          ) {
            localityId = datasetFeature.datasetAttributes['ADM3_PCODE'];
          } else {
            localityId = datasetFeature.datasetAttributes['ADM4_PCODE'];
          }

          return {
            strokeColor: selectedLocality === localityId ? 'black' : undefined,
            strokeWeight: 3.0,
            fillColor: data.barangays[localityId].color,
            fillOpacity: 0.3
          };
        } catch {
          return {
            // strokeColor: 'black',
            strokeWeight: 1.0,
            fillColor: 'gray',
            fillOpacity: 0.3
          };
        }
      }
    }

    function buildElement(name: string, value: number) {
      const element = document.createElement('div');
      element.className = 'bg-zinc-900 p-2 rounded-lg font-bold text-white text-center';

      let innerHTML = `<h1 class="text-md">${name}</h1>`;

      if (value) {
        innerHTML += `<p class="text-lg font-extrabold">${formatCurrency(
          value
        )} <span class="text-xs">avg price</span></p>`;
      }

      element.innerHTML = innerHTML;

      return element;
    }

    async function handleClick(e) {
      //@ts-ignore
      const { AdvancedMarkerElement } = (await google.maps.importLibrary(
        'marker'
        //@ts-ignore
      )) as google.maps.MarkerLibrary;
      const datasetFeature = e.features[0];
      const adminLevel2 = datasetFeature.datasetAttributes['ADM2_EN'];

      let idValue;

      if (adminLevel2 === 'NCR, CITY OF MANILA, FIRST DISTRICT (Not a Province)') {
        idValue = datasetFeature.datasetAttributes['ADM3_PCODE'];
      } else {
        idValue = datasetFeature.datasetAttributes['ADM4_PCODE'];
      }

      for (let i = 0; i < allMarkers.length; i++) {
        allMarkers[i].setMap(null);
      }

      const marker = new AdvancedMarkerElement({
        map,
        position: data.barangays[idValue].position,
        content: buildElement(data.barangays[idValue].name, data.barangays[idValue].value)
      });

      allMarkers.push(marker);

      const datasetLayer = map.getDatasetFeatureLayer(data.BARANGAYS_DATASET_ID);
      selectedLocality = idValue;
      datasetLayer.style = setStyle;
    }

    loader.load().then(async () => {
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

      // if (currentLevel === 'city') {
      //   for (const city of Object.keys(cities)) {
      //     if (cities[city].position.lat !== 0) {
      //       const marker = new AdvancedMarkerElement({
      //         map,
      //         position: cities[city].position,
      //         content: buildElement(cities[city].name, cities[city].value)
      //       });
      //     }
      //   }
      // } else {
      //   for (const brgy of Object.keys(barangays)) {
      //     if (barangays[brgy].position.lat !== 0) {
      //       const marker = new AdvancedMarkerElement({
      //         map,
      //         position: barangays[brgy].position,
      //         content: buildElement(barangays[brgy].name, barangays[brgy].value)
      //       });
      //     }
      //   }
      // }
    });
  });
</script>

<div class="flex h-full flex-col bg-zinc-900">
  <script
    async
    src={`https://maps.googleapis.com/maps/api/js?key=${data.MAPS_API_KEY}&callback=initMap&v=beta`}></script>
  <div class="flex">
    <h1 class="text-white">landvalue.ph</h1>
    <div>
      <select name="viewing" id="inputViewing" bind:value={currentLevel}>
        <option value="city">City</option>
        <option value="district">District</option>
      </select>
    </div>
  </div>
  <div id="map" class="h-full" />
</div>
