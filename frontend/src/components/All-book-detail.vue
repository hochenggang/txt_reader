<template>
  <div class="full">
    <p>{{b.b.book_name}}</p>
    <p>{{b.b.book_size}}</p>
    <p>{{b.b.book_upload_time}}</p>
    <p>{{b.b.book_status}}</p>

    <span class="exit" v-on:click="b.show_book_detail = !b.show_book_detail">
      <svg role="img" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" aria-labelledby="cancelIconTitle">
        <path d="M15.5355339 15.5355339L8.46446609 8.46446609M15.5355339 8.46446609L8.46446609 15.5355339"></path>
        <path d="M4.92893219,19.0710678 C1.02368927,15.1658249 1.02368927,8.83417511 4.92893219,4.92893219 C8.83417511,1.02368927 15.1658249,1.02368927 19.0710678,4.92893219 C22.9763107,8.83417511 22.9763107,15.1658249 19.0710678,19.0710678 C15.1658249,22.9763107 8.83417511,22.9763107 4.92893219,19.0710678 Z"></path>
      </svg>
    </span>
  </div>
</template>

<script>

export default {
  name: "AllBookDetail",
  props: {
    b: Object
  },

  methods: {
    
  }
};
</script>

<style scoped>

.full {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  overflow-y: auto;
  -webkit-overflow-scrolling: touch;
  padding: 0.5rem;

  background-color: rgb(250, 235, 215);
}

.exit {
  position: absolute;
  bottom: 1rem;
  left: calc(50% - .5rem);
}
</style>
