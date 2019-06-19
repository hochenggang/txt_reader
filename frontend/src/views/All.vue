<template>
  <div class="w-75">
    <Loading v-if="loading"/>
    <div>
      <div class="head">
        <p>Reader</p>
        <div class="head-icon">
          <span title="刷新" v-on:click="get_books"  class="icon-link">
            <svg
              role="img"
              xmlns="http://www.w3.org/2000/svg"
              width="24"
              height="24"
              viewBox="0 0 24 24"
              aria-labelledby="refreshIconTitle"
            >
              <polyline points="22 12 19 15 16 12"></polyline>
              <path
                d="M11,20 C6.581722,20 3,16.418278 3,12 C3,7.581722 6.581722,4 11,4 C15.418278,4 19,7.581722 19,12 L19,14"
              ></path>
            </svg>
          </span>
          <router-link class="icon-link" to="/upload">
            <span title="上传" class="icon-link">
              <svg
                width="24"
                height="24"
                viewBox="0 0 24 24"
                xmlns="http://www.w3.org/2000/svg"
                aria-labelledby="shareIconTitle"
              >
                <path d="M12 14V6"></path>
                <path d="M9 8L12 5L15 8"></path>
                <path d="M5 13V18H19V13"></path>
              </svg>
            </span>
          </router-link>
          <span title="退出" class="icon-link" v-on:click="logout">
            <svg
              role="img"
              xmlns="http://www.w3.org/2000/svg"
              width="24"
              height="24"
              viewBox="0 0 24 24"
              aria-labelledby="exitIconTitle"
            >
              <path d="M18 15l3-3-3-3"></path>
              <path d="M11.5 12H20"></path>
              <path stroke-linecap="round" d="M21 12h-1"></path>
              <path d="M15 4v16H4V4z"></path>
            </svg>
          </span>
        </div>
      </div>
      <p class="c" v-if="error">{{errmsg}}</p>
      <ul class="books">
        <li class="book" v-for="b in this.books" :key="b.book_id">
          <span v-if="b.book_status == 0" class="book_name_1">已上传 {{b.book_name}}</span>
          <span v-if="b.book_status == 2" class="book_name_1">解析中 {{b.book_name}}</span>
          <span v-if="b.book_status == -1" class="book_name_1">解析失败 {{b.book_name}}</span>
          <span v-if="b.book_status == -2" class="book_name_1">解码失败 {{b.book_name}}</span>
          <router-link :to="{ path: 'reader', query: { id: b.book_id }}" v-if="b.book_status == 1" class="book_name_2">{{b.book_name}}</router-link>
        </li>
      </ul>
    </div>

  </div>
</template>

<script>
import axios from "axios";
import Loading from "@/components/Loading.vue";

export default {
  name: "all",
  components: {
    Loading,
  },
  data: function() {
    return {
      mail: "",
      password: "",
      loading: false,
      error: false,
      errmsg: "",
      books: []
    };
  },
  mounted: function() {
    this.get_books();
  },
  methods: {
    get_books: function() {
      this.loading = true;
      axios
        .get("/api/book/books", {
          headers: {
            "x-user-id": localStorage["txt_reader_user_id"],
            "x-user-key": localStorage["txt_reader_user_key"]
          }
        })
        .then(response => {
          this.books = response.data;
        })
        .catch(error => {
          if (error.response.status == 404) {
            this.error = true;
            this.errmsg = "快去上传一本书籍吧";
          }
        })
        .finally(() => {
          this.loading = false;
        });
    },
    logout:function(){
      delete localStorage["txt_reader_user_id"];
      delete localStorage["txt_reader_user_key"];
      location.assign("/");
    }
  }
};
</script>

<style>
.w-75 {
  display: block;
  width: 75%;
  margin: 0 auto;
}
@media screen and (max-width: 720px) {
  .w-75 {
    width: 100%;
  }
}
.head {
  display: flex;
  justify-content: space-between;
  line-height: 2rem;
  padding: 0.5rem;
}
.book {
  list-style: none;
  display: flex;
  justify-content: space-between;
  padding: .75rem 0;
  border-top: 1px solid #ffffff;
}
.book_name_1,.book_name_2,.book_name_3 {
  display: inline-block;
  max-width: 15rem;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.book_name_1 {
  color: #ee3f4d;
}
.head-icon {
  display: flex;
  flex-wrap: nowrap;
}
.icon-link {
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
}
svg {
  margin: 0 0.25rem;
  width: 1.5rem;
  height: 1.5rem;
  stroke: #1a2a3a;
  stroke-width: 1;
  stroke-linecap: square;
  stroke-linejoin: miter;
  fill: none;
  color: #1a2a3a;
}
.books {
  padding: 0.5rem;
  overflow-y: auto;
}
</style>

