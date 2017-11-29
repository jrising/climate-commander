$(".stop_job").click(function(){
    job_name = $(this).parents('h3').text();
    $.ajax({
        type: "POST",
        url: "/stop_job/",
        data:{
            job_name: job_name
        },
        success: function(ret){

        }
    });
});

$(".delete_jobrun").click(function(){
    jobrun_id = $(this).attr('data')
    var $tr = $(this).parents('tr');
    $.ajax({
        type: "POST",
        url: "/delete_jobrun/",
        data: {
            id: jobrun_id
        },
        success: function(ret){
	    $tr.slideUp();
        }
    });
});
