new Vue({
    el: '#poll',
    data: {
        poll: [],
    },
    created: function() {
        const app = this;
        axios.get('/api/poll/').then(function(response) {
            app.poll = response.data;
        })
    },
})
new Vue({
    el: '#question',
    data: {
        question: [],
    },
    created: function() {
        const app = this;
        axios.get('/api/question/').then(function(response) {
            app.question = response.data;
        })
    },
})

new Vue({
  el: '#reg',
  data: {
    checkedNames: [],
    checkedPassword: [],
  }
})