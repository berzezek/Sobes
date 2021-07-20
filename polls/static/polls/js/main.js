new Vue({
    el: '#polls',
    data: {
        polls: [],
        num: 0,

    },
    created: function() {
        const app = this;
        axios.get('/api/v1/poll/').then(function(response) {
            app.polls = response.data;
        })
    },
})
