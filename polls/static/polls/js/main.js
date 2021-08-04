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
    }
});

new Vue({
    el: '#user_answer',
    data: {
        user_answer: [],
    },
    created: function() {
        const app = this;
        axios.get('/api/user_answer/').then(function(response) {
            app.user_answer = response.data;
        })
    }
});
