import { env } from '$env/dynamic/private';
import cities from '$lib/data/cities.json';
import barangays from '$lib/data/barangays.json';

export async function load() {
  return {
    cities,
    barangays,
    MAPS_API_KEY: env.MAPS_API_KEY,
    MAP_ID: env.MAP_ID,
    BARANGAYS_DATASET_ID: env.BARANGAYS_DATASET_ID
  };
}
