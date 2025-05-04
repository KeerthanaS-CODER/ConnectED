// Patents by Faculty
const patentsCtx = document.getElementById('patentsChart').getContext('2d');
new Chart(patentsCtx, {
    type: 'bar',
    data: {
        labels: ['Jayanthi', 'Srinivasan', 'Vidhya'],
        datasets: [{
            label: 'Number of Patents',
            data: [3, 2, 1],
            backgroundColor: ['#66c2a5', '#fc8d62', '#8da0cb']
        }]
    },
    options: {
        scales: {
            y: { beginAtZero: true }
        }
    }
});

// Competitions by Faculty
const competitionsCtx = document.getElementById('competitionsChart').getContext('2d');
new Chart(competitionsCtx, {
    type: 'bar',
    data: {
        labels: ['Kiruthika Devi', 'Vidhya', 'Anitha'],
        datasets: [{
            label: 'Number of Competitions',
            data: [6, 3, 2],
            backgroundColor: ['#e78ac3', '#a6d854', '#ffd92f']
        }]
    },
    options: {
        scales: {
            y: { beginAtZero: true }
        }
    }
});

// Publications by Faculty
const publicationsCtx = document.getElementById('publicationsChart').getContext('2d');
new Chart(publicationsCtx, {
    type: 'bar',
    data: {
        labels: ['Jayanthi', 'Sanjay', 'Vidhya'],
        datasets: [{
            label: 'Number of Publications',
            data: [2, 2, 1],
            backgroundColor: ['#66c2a5', '#fc8d62', '#8da0cb']
        }]
    },
    options: {
        scales: {
            y: { beginAtZero: true }
        }
    }
});

// Grants by Faculty
const grantsCtx = document.getElementById('grantsChart').getContext('2d');
new Chart(grantsCtx, {
    type: 'bar',
    data: {
        labels: ['Ramya', 'Sivagami', 'Vidhya'],
        datasets: [{
            label: 'Number of Grants',
            data: [2, 1, 1],
            backgroundColor: ['#66c2a5', '#fc8d62', '#8da0cb']
        }]
    },
    options: {
        scales: {
            y: { beginAtZero: true }
        }
    }
});

// Research Projects by Department
const researchProjectsDeptCtx = document.getElementById('researchProjectsDeptChart').getContext('2d');
new Chart(researchProjectsDeptCtx, {
    type: 'line',
    data: {
        labels: ['CSE', 'ECE', 'IT', 'EEE', 'AIDS', 'CIVIL'],
        datasets: [{
            label: 'Research Projects',
            data: [6, 5, 4, 3, 2, 1],
            backgroundColor: '#ff9999',
            borderColor: '#ff6666',
            fill: true
        }]
    },
    options: {
        scales: {
            y: { beginAtZero: true }
        }
    }
});

// Competitions by Department
const competitionsDeptCtx = document.getElementById('competitionsDeptChart').getContext('2d');
new Chart(competitionsDeptCtx, {
    type: 'bar',
    data: {
        labels: ['CSE', 'IT', 'CIVIL', 'ECE', 'EEE', 'AIDS'],
        datasets: [{
            label: 'Competitions',
            data: [5, 4, 3, 2, 1, 0],
            backgroundColor: '#99c2ff'
        }]
    },
    options: {
        scales: {
            y: { beginAtZero: true }
        }
    }
});

// Publications by Department
const publicationsDeptCtx = document.getElementById('publicationsDeptChart').getContext('2d');
new Chart(publicationsDeptCtx, {
    type: 'line',
    data: {
        labels: ['CSE', 'ECE', 'IT', 'EEE', 'AIDS', 'CIVIL'],
        datasets: [{
            label: 'Publications',
            data: [20, 15, 10, 5, 3, 2],
            backgroundColor: '#66c2a5',
            borderColor: '#66c2a5',
            fill: true
        }]
    },
    options: {
        scales: {
            y: { beginAtZero: true }
        }
    }
});

// Awards by Department
const awardsDeptCtx = document.getElementById('awardsDeptChart').getContext('2d');
new Chart(awardsDeptCtx, {
    type: 'bar',
    data: {
        labels: ['CSE', 'IT', 'ECE', 'EEE', 'AIDS', 'CIVIL'],
        datasets: [{
            label: 'Awards',
            data: [4, 3, 2, 1, 0, 0],
            backgroundColor: '#ffcc99'
        }]
    },
    options: {
        scales: {
            y: { beginAtZero: true }
        }
    }
});

// Faculty Count by Department (Pie Chart)
const facultyCountDeptCtx = document.getElementById('facultyCountDeptChart').getContext('2d');
new Chart(facultyCountDeptCtx, {
    type: 'pie',
    data: {
        labels: ['CSE', 'ECE', 'IT', 'EEE', 'AIDS', 'CIVIL'],
        datasets: [{
            label: 'Faculty Count',
            data: [23, 20, 15, 13, 10, 8],
            backgroundColor: ['#ff9999', '#66c2a5', '#fc8d62', '#8da0cb', '#ffd92f', '#e78ac3']
        }]
    },
    options: {}
});
