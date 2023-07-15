import { readdirSync, readFile, readFileSync, writeFileSync } from 'fs';

const geodataFiles = readdirSync('./geodata');

let features: any[] = [];

for (const filename of geodataFiles) {
  const barangayFile = readFileSync(`./geodata/${filename}`);
  const data = JSON.parse(barangayFile.toString());

  if (data.features[0]['properties']['ADM1_PCODE'] === 'PH130000000') {
    features = [...features, ...data['features']];
  }
}

const finalData = {
  type: 'FeatureCollection',
  features
};

writeFileSync('./consolidated.json', JSON.stringify(finalData));
