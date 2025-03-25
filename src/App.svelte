<script>
  import Router from "svelte-spa-router";
  import Login from "./pages/Login.svelte";
  import Main from "./pages/Main.svelte";
  import Signup from "./pages/Signup.svelte";
  import Write from "./pages/Write.svelte";
  import NotFound from "./pages/NotFound.svelte";
  import "./css/main.css";
  import GatherTown from "./pages/GatherTown.svelte";
  import WordSearch from "./pages/WordSearch.svelte";

  const routes = {
    "/": Main,
    "/login": Login,
    "/signup": Signup,
    "/write": Write,
    "/gather-town": GatherTown,
    "/word-search": WordSearch,
    "*": NotFound,
  };
</script>

<Router {routes} />
