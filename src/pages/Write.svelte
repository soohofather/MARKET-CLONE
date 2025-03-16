

<script>
  import { getDatabase, ref, push } from "firebase/database";
  import Footer from "../components/Footer.svelte";

  let title;
  let price;
  let description;
  let place;

function writeUserData(event) {
  const db = getDatabase();
  push(ref(db, 'items/'), {
    title,
    price,
    description,
    place
  });
  window.location.hash = "/";
}

</script>

<form id="write-form" on:submit|preventDefault={writeUserData}>
  <!-- <div>
    <label for="image">이미지</label>
    <input type="file" id="image" name="image" />
  </div> -->
  <div>
    <label for="title">제목</label>
    <input type="text" id="title" name="title" bind:value={title}/>
  </div>
  <div>
    <label for="price">가격</label>
    <input type="number" id="price" name="price" bind:value={price}/>
  </div>
  <div>
    <label for="description">설명</label>
    <input type="text" id="description" name="description" bind:value={description}/>
  </div>
  <div>
    <label for="place">장소</label>
    <input type="text" id="place" name="place" bind:value={place}/>
  </div>
  <div>
    <input class = "write-button" type="submit" />
  </div>
</form>

<Footer location = "write"/>

<style>

  .write-button {
    background-color: tomato;
    margin: 10px;
    border-radius: 10px;
    padding: 5px 12px 5px 12px;
    color: white;
    cursor: pointer;
  }

</style>
