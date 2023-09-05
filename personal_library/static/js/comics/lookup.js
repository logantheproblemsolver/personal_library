const addButton = document.getElementById('addButton');


async function addComicToLibrary(title, series_number, desc, image, volume) {
  console.log("comic info", title, series_number, desc, image, volume)
  const comicBookData = {
    title, series_number, desc, image, volume
  }
  const response = await fetch("/comics/lookup/add", {
    method: "POST",
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(comicBookData),
  })

  if (response.status != 200) {
    console.log("something we wrong", response.status)
    return;
  }

  const data = await response.json()
  console.log(data);

}