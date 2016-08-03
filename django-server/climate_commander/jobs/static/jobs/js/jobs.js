$("#job_selected").change(function(){
    job_selected = $("select option:selected").text();
    console.log(job_selected);
    
    // $.ajax({
    //     url: "/run_ajax/",
    //     type: "POST",
    //     data: {job_selected: job_selected},
    //     success: function(){
    //         console.log("Yo");
    //     },
    //     error: function(){
    //         console.log("Da-Da!!");
    //     }
    // });
});
