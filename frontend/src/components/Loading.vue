<template>
  <div class="loading">
      <div class="loading-circle"></div>
  </div>
</template>

<style scoped>

.loading {
    display: flex;
    position: fixed;
    top: 0;
    left: 0;
    bottom: 0;
    right: 0;
    justify-content: center;
    align-items: center;
    background-color: #f7f4ed;
    z-index: 1;
}

.loading-circle {
    width: 1.5rem;
    height: 1.5rem;
    border-radius: 50%;
    border: .25rem solid #34495e;
    animation: spin 1.5s ease-in-out infinite;
}

@keyframes spin {
    to {
        transform: rotateY(540deg);
    }
}

</style>
