// generate array
function generateArray(color, length) {
    return Array.from({ length }, () => color);
  }

// element id , title of chart , data, type
function createChart(element_id,title,data,type) 
{
    let data_new = '';
    let legend_display = false;
    let label_string = '';
    let scale_label=false;
    let axis_scale= false;
    var parent_div = $('#' + element_id).parent();
    $('#' + element_id).remove();
    parent_div.append('<canvas id="' + element_id + '" height="350"></canvas>');
    var ctx = document.getElementById(element_id);

    if(element_id === 'gender_distribution_chart'){

        let customBackgroundColor1 = generateArray('brown', 12);
        let customBackgroundColor2 = generateArray('green', 12);
        let customBackgroundColor3 = generateArray('blue', 12);

        legend_display = true;
        axis_scale=true;
        scale_label=true;
        label_string = 'Province';

        data_labels =[];
        data_male_count=[];
        data_female_count=[];
        data_total_count=[];

        //loop through data to make datasets
        $.each(data,function(province,data){
            data_labels.push(province);
            data_male_count.push(data.Male)
            data_female_count.push(data.Female)
            data_total_count.push(data.Male+data.Female)
        })
        data_new= {
            labels: data_labels,
            datasets: [{    
                label: 'Male',
                data: data_male_count,
                maxBarThickness: 10,
                categoryPercentage: 0.3,
                barPercentage:1,
                backgroundColor: customBackgroundColor1,
            },
            {
                label: 'Female',
                data: data_female_count,
                maxBarThickness: 10,
                categoryPercentage: 0.3,
                barPercentage:1,
                backgroundColor: customBackgroundColor2,
            },
            {
                label: 'Total',
                data: data_total_count,
                maxBarThickness: 10,
                categoryPercentage: 0.3,
                barPercentage:1,
                backgroundColor: customBackgroundColor3,
            }]
        };
    }
    var myChart = new Chart(ctx, {
        type: type,
        data:data_new,
        options: {
            responsive: true,
            title: {
                display: true,
                text: title,
                fontSize: 15,
                fontColor:'black',
                fontFamily:'Cursive',
            },
            animation: {
                animateScale: true,
                animateRotate: true
            },
            tooltips: {
                enabled :true,
                mode: 'single',
                displayColors:true,
                titleFontSize:13,
                titleFontFamily:'Cursive',
                bodyFontSize:12,
                bodyFontFamily:'Cursive',
                callbacks: {
                    label: function(tooltipItem, data) {
                        var label1 = data.datasets[tooltipItem.datasetIndex].label;
                        label1 += ' : '+data.datasets[tooltipItem.datasetIndex].data[tooltipItem.index];
                        return label1;
                    },
                }
            },
            legend: {
                display: legend_display,
                position:'top',
                labels: {
                    fontColor: 'black',
                    fontFamily:'Cursive',
                    fontSize:12
                }
            },
            scales: {
                yAxes: [{
                    display:axis_scale,
                    ticks: {
                        beginAtZero: true,
                        fontFamily:'Cursive',
                        fontColor:'black'
                    },
                    scaleLabel: {
                        display: scale_label,
                        labelString: 'Number'
                    }
                }],
                xAxes: [{
                    display:axis_scale,
                    scaleLabel: {
                        display: scale_label,
                        labelString: label_string
                    }
                }],
            }
        },
    });
}