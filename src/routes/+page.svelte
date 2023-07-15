<script lang="ts">
  import { formatAmountToCurrency } from '$lib/utils.js';
  import { Loader } from '@googlemaps/js-api-loader';
  import { onMount } from 'svelte';

  let currentLevel: 'city' | 'district' = 'city';

  export let data;

  const { cities, MAPS_API_KEY, MAP_ID, BARANGAYS_DATASET_ID } = data;

  onMount(() => {
    const loader = new Loader({
      apiKey: MAPS_API_KEY,
      version: 'beta'
    });

    function setStyle(params: any) {
      const datasetFeature = params.feature;

      if (currentLevel === 'city') {
        const adminLevel2 = datasetFeature.datasetAttributes['ADM2_EN'];

        let value;

        if (adminLevel2 === 'NCR, CITY OF MANILA, FIRST DISTRICT (Not a Province)') {
          value = cities['CITY OF MANILA'].color;
        } else {
          const city = datasetFeature.datasetAttributes['ADM3_EN'] as string;
          value = cities[city].color;
        }

        return {
          strokeWeight: 3.0,
          fillColor: value,
          fillOpacity: 0.3
        };
      } else if (currentLevel === 'district') {
        const adminLevel2 = datasetFeature.datasetAttributes['ADM2_EN'];

        // const rawDistrict = datasetFeature.datasetAttributes['ADM4_EN'];
        let rawDistrict;

        let value;

        if (adminLevel2 === 'NCR, CITY OF MANILA, FIRST DISTRICT (Not a Province)') {
          rawDistrict = datasetFeature.datasetAttributes['ADM3_EN'] as string;
        } else {
          rawDistrict = datasetFeature.datasetAttributes['ADM4_EN'] as string;
        }

        if (Object.keys(masterDataDistrict).includes(rawDistrict)) {
          value = masterDataDistrict[rawDistrict];
        } else {
          masterDataDistrict[rawDistrict] = Math.random() < 0.5 ? 'green' : 'red';
        }

        return {
          strokeWeight: 3.0,
          fillColor: value,
          fillOpacity: 0.3
        };
      }
    }

    loader.load().then(async () => {
      const { Map } = (await google.maps.importLibrary('maps')) as google.maps.MapsLibrary;
      const { AdvancedMarkerElement } = (await google.maps.importLibrary(
        'marker'
      )) as google.maps.MarkerLibrary;

      const map = new Map(document.getElementById('map') as HTMLElement, {
        center: { lat: 14.5964947, lng: 120.9883602 },
        zoom: 12,
        mapId: MAP_ID,
        mapTypeControl: false
      });

      const datasetLayer = map.getDatasetFeatureLayer(BARANGAYS_DATASET_ID);
      datasetLayer.style = setStyle;

      for (const city of Object.keys(cities)) {
        if (cities[city].position.lat !== 0) {
          // new google.maps.Marker({
          //   position: cities[city].position,
          //   map,
          //   icon: {
          //     path: google.maps.SymbolPath.CIRCLE,
          //     scale: 0
          //   },
          //   draggable: false,
          //   label: { text: `${cities[city].name}`, color: 'white', fontWeight: 'bold' }
          // });

          // const valuePosition = {
          //   lat: cities[city].position.lat - 0.005,
          //   lng: cities[city].position.lng
          // };

          // new google.maps.Marker({
          //   position: valuePosition,
          //   map,
          //   icon: {
          //     path: google.maps.SymbolPath.CIRCLE,
          //     scale: 0
          //   },
          //   draggable: false,
          //   label: {
          //     text: `${formatAmountToCurrency(cities[city].value, '₱')} /sq. m.`,
          //     color: 'white',
          //     fontWeight: 'bold'
          //   }
          // });

          const priceTag = document.createElement('div');
          priceTag.className = 'bg-zinc-900 p-2 rounded-lg font-bold text-white text-center';
          priceTag.innerHTML = `<h1 class="text-md">${
            cities[city].name
          }</h1><p class="text-lg font-extrabold">${formatAmountToCurrency(
            cities[city].value,
            '₱'
          )} <span class="text-sm">per sqm</span></p>`;

          const marker = new AdvancedMarkerElement({
            map,
            position: cities[city].position,
            content: priceTag
          });
        }
      }
    });
  });
</script>

<div class="flex h-full flex-col bg-zinc-900">
  <script
    async
    src={`https://maps.googleapis.com/maps/api/js?key=${MAPS_API_KEY}&callback=initMap&v=beta`}></script>
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
