new Vue({
    el: '#poll',
    data: {
        poll: [],
        url: 'polls',
    },
    created: function() {
        const app = this;
        axios.get('/polls/').then(function(response) {
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
        axios.get('/question/').then(function(response) {
            app.question = response.data;
        })
    },
})


new Vue({
    el: '#answer-choice',
    data: {
        answer-choice: [],
    },
    created: function() {
        const app = this;
        axios.get('/answer-choice/').then(function(response) {
            app.answer-choice = response.data;
        })
    },
})


new Vue({
    el: '#user-answer',
    data: {
        user-answer: [],
    },
    created: function() {
        const app = this;
        axios.get('/user-answer/').then(function(response) {
            app.user-answer = response.data;
        })
    },
})
