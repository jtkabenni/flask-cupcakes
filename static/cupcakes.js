const base_url = "http://127.0.0.1:5000/api";
const form = document.querySelector("form");

async function showCupcakeList() {
  const response = await axios.get(`${base_url}/cupcakes`);
  const data = response.data;
  for (let cupcake of data.cupcakes) {
    createCupcake(cupcake);
  }
}

form.addEventListener("submit", async function (evt) {
  evt.preventDefault();
  let flavor = document.querySelector("#flavor").value;
  let size = document.querySelector("#size").value;
  let rating = document.querySelector("#rating").value;
  let image = (document.querySelector("#image").value = ""
    ? Null
    : document.querySelector("#image").value);

  const response = await axios.post(`${base_url}/cupcakes`, {
    flavor: flavor,
    size: size,
    rating: rating,
    image: image,
  });
  const data = response.data;

  createCupcake(data.cupcake);
  form.reset();
});

function createCupcake(cupcake) {
  const cupcakes = document.querySelector(".cupcakes");
  const div = document.createElement("div");
  const img = document.createElement("img");
  img.src = cupcake.image;
  const title = document.createElement("p");

  title.innerHTML = `${cupcake.flavor} - ${cupcake.size} - ${cupcake.rating} stars`;
  if (cupcake.image) {
    div.append(img);
  }
  cupcakes.append(title);
  cupcakes.append(div);
}

showCupcakeList();
