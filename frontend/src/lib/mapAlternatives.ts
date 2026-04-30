export function openStreetMapUrl(lat: number, lng: number, zoom = 18): string {
  return `https://www.openstreetmap.org/?mlat=${lat}&mlon=${lng}#map=${zoom}/${lat}/${lng}`;
}

export function openStreetMapStaticUrl(lat: number, lng: number, zoom = 18): string {
  return (
    `https://staticmap.openstreetmap.de/staticmap.php` +
    `?center=${lat},${lng}` +
    `&zoom=${zoom}` +
    `&size=640x400` +
    `&markers=${lat},${lng},red-pushpin`
  );
}
