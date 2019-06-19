<template>
  <div id="app">
    <router-view/>
  </div>
</template>

<style>

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html {
  font-size: 16px;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
body {
  background-color: #f7f4ed;
}

p {
  font-size: 1rem;
  line-height: 2rem;
  font-weight: normal;
  color: #1a2a3a;
}

a,
a:visited {
  color: #91b0e4;
  text-decoration: none;
}

input {
  border: none;
  padding: 0.5rem;
  width: 100%;
  outline: none;
}

.btn {
  display: inline-block;
  border: none;
  padding: 0.5rem 0.75rem;
  margin: 0.25rem;
  border-radius: 0.25rem;
  margin-right: 0.25rem;
}

</style>
