<template>
  <!-- 目录 -->
  <ul v-if="now.catalog" class="readerCatalogue" v-scollTop>
    <div class="readerCatalogueContent">
      <li
        v-for="index in range(page*pageCapacity-pageCapacity,page*pageCapacity<totalIndex?page*pageCapacity:totalIndex)"
        @click="now.index=index,now.show_catalogue = false"
        :key="index"
      >
        <p class="catalogueText">{{ now.catalog[index][1] }}</p>
      </li>
    </div>

    <div class="readerCatalogueControlBar">
      <p @click="page>1? page--:page=1,cusPage=page">上一页</p>
      <p>
        <input
          type="text"
          v-model="cusPage"
          @keypress.enter="loadCusPage"
          :placeholder="'1 - '+this.maxPage"
        >
      </p>
      <p @click="page<maxPage? page++:page=maxPage,cusPage=page">下一页</p>
    </div>

    <div class="readerCatalogueMask" @click="now.show_catalogue=false"></div>
  </ul>
</template>

<script>

export default {
  name: "Reader_catalogue",
  directives: {
    scollTop: {
      update: function(el) {
        el.scrollTop = 0;
      }
    }
  },
  props: {
    now: Object
  },
  mounted: function() {
    this.totalIndex = this.now.catalog.length;
    // 章节量/每页容量=最大页数
    this.maxPage = Math.floor(this.totalIndex / this.pageCapacity) + 1;
    this.page = Math.floor(this.now.index / this.pageCapacity) + 1;
  },
  data: function() {
    return {
      totalIndex: null,
      page: 1,
      pageCapacity: 50,
      maxPage: null,
      cusPage: null,
    };
  },

  methods: {
    loadCusPage: function() {
      if (!(this.cusPage && this.maxPage)) {
        return false;
      }
      if (this.cusPage <= this.maxPage && this.cusPage > 0) {
        this.page = this.cusPage;
      }
    },
    range: function(start, end) {
      if (end - start > 0) {
        let container = [];
        while (start < end) {
          container.push(start);
          start += 1;
        }
        return container;
      }
    }
  }
};
</script>

<style scoped>

.readerCatalogueContent {
  z-index: 4;
  position: fixed;
  top: 5%;
  left: 10%;
  right: 10%;
  bottom: 10%;
  overflow-y: auto;
  -webkit-overflow-scrolling: touch;
  padding: 0.5rem;

  background-color: #f7f4ed;

  box-shadow: 0px -1px 8px 0px rgba(155, 155, 155, 0.5);
}

.catalogueText {
  font-size: .9rem;
  line-height: 1rem;
  font-weight: lighter;
  color: #1a2a3a;
}

.readerCatalogueControlBar {
  position: fixed;
  top: 90%;
  left: 10%;
  right: 10%;
  height: 5%;
  min-height: 30px;
  background-color: #f7f4ed;

  box-shadow: 0px -1px 8px 0px rgba(155, 155, 155, 0.5);

  display: flex;
  justify-content: space-between;

  z-index: 4;
}
.readerCatalogueControlBar p {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 33.3%;
  line-height: 100%;
  cursor: pointer;
  font-size: 0.7rem;
  font-weight: lighter;
}

input {
  width: 100%;
  background: transparent;
  border: 1px solid #fff;
  border-radius: 1rem;
  outline: none;
  font-size: 0.8rem;
  padding: 2.5px;
  text-align: center;
  font-weight: lighter;
}

.readerCatalogue li {
  display: flex;
  justify-content: space-between;
  margin-top: 10px;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid #fff;
  cursor: pointer;
  font-size: 0.9rem;
}

.readerCatalogueMask {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 3;
}
</style>
