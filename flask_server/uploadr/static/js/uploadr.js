/******************************************************************************
 * HTML5 Multiple File Uploader Demo                                          *
 ******************************************************************************/

// Constants
// Change this is current space left on USB. Update it after each upload
var MAX_UPLOAD_FILE_SIZE = 1024*1024; // 1 MB
//change this to usb drive.
var NEXT_URL   = "/";

// List of pending files to handle when the Upload button is finally clicked.
var PENDING_FILES  = [];

function handle_file_change(event) {
      	var url = $(this).parent().parent().parent().attr("action");
        handleFiles(this.files);
        doUpload(url);

}
$(document).ready(function() {
    // Set up the drag/drop zone.
    var ii;
    for (ii = 1; ii < 5; ii++) {
    	initDropbox(ii);
        $("#file-picker-" + ii).on("change", handle_file_change);

    }

	/*
    // Handle the submit button.
    $("#upload-button").on("click", function(e) {
        // If the user has JS disabled, none of this code is running but the
        // file multi-upload input box should still work. In this case they'll
        // just POST to the upload endpoint directly. However, with JS we'll do
        // the POST using ajax and then redirect them ourself when done.
        e.preventDefault();
        doUpload();
    })
*/
});


function doUpload(url) {
    $("#progress").show();
    var $progressBar   = $("#progress-bar");

    // Gray out the form.
    $("#upload-form :input").attr("disabled", "disabled");

    // Initialize the progress bar.
    $progressBar.css({"width": "0%"});

    // Collect the form data.
    fd = collectFormData();

    // Attach the files.
    for (var i = 0, ie = PENDING_FILES.length; i < ie; i++) {
        // Collect the other form data.
        fd.append("file", PENDING_FILES[i]);
    }

    // Inform the back-end that we're doing this over ajax.
    fd.append("__ajax", "true");

    var xhr = $.ajax({
        xhr: function() {
            var xhrobj = $.ajaxSettings.xhr();
            if (xhrobj.upload) {
                xhrobj.upload.addEventListener("progress", function(event) {
                    var percent = 0;
                    var position = event.loaded || event.position;
                    var total    = event.total;
                    if (event.lengthComputable) {
                        percent = Math.ceil(position / total * 100);
                    }

                    // Set the progress bar.
                    $progressBar.css({"width": percent + "%"});
                    $progressBar.text(percent + "%");
                }, false)
            }
            return xhrobj;
        },
        url: url,
        method: "POST",
        contentType: false,
        processData: false,
        cache: false,
        data: fd,
        success: function(data) {
            $progressBar.css({"width": "100%"});
            location.reload(true);
        },
    });
}


function collectFormData() {
    // Go through all the form fields and collect their names/values.
    var fd = new FormData();

    $("#upload-form :input").each(function() {
        var $this = $(this);
        var name  = $this.attr("name");
        var type  = $this.attr("type") || "";
        var value = $this.val();
        fd.append(name, value);
    });

    return fd;
}


function handleFiles(files) {
    // Add them to the pending files list.
    for (var i = 0, ie = files.length; i < ie; i++) {
        PENDING_FILES.push(files[i]);
    }
}

function updateAvailableFiles()
{
    var $dropbox = $("#dropbox");
    $dropbox.html("")
    $dropbox.append('<table>')     
    $dropbox.append('<tr><td colspan="1"><td>');
    $dropbox.append('Pending Uploads:');
    $dropbox.append('</td></tr>');
    var i;
    for(i=0; i < PENDING_FILES.length; i++)
    {
        $dropbox.append('<tr><td colspan="1"><td>');
        $dropbox.append(PENDING_FILES[i].name);
        $dropbox.append('</td></tr>');
    }     
    $dropbox.append('</table>')   

}
function initDropbox(number) {
    var $dropbox = $("#dropbox" + number);

    // On drag enter...
    $dropbox.on("dragenter", function(e) {
        e.stopPropagation();
        e.preventDefault();
        $(this).addClass("active");
    });

    // On drag exit...
    $dropbox.on("dragexit", function(e) {
        e.stopPropagation();
        e.preventDefault();
        $(this).removeClass("active");
    });

    // On drag exit...
    $dropbox.on("dragleave", function(e) {
        e.stopPropagation();
        e.preventDefault();
        $(this).removeClass("active");
    });

    // On drag over...
    $dropbox.on("dragover", function(e) {
        e.stopPropagation();
        e.preventDefault();
    });

    // On drop...
    $dropbox.on("drop", function(e) {
        e.preventDefault();
        $(this).removeClass("active");

        // Get the files.
        var files = e.originalEvent.dataTransfer.files;
        handleFiles(files);
        doUpload($(this).parent().attr("action"));
       // updatePendingFileText();
        //$dropbox.text(PENDING_FILES.length + " files ready for upload!");
         
    });

    

    // If the files are dropped outside of the drop zone, the browser will
    // redirect to show the files in the window. To avoid that we can prevent
    // the 'drop' event on the document.
    function stopDefault(e) {
        e.stopPropagation();
        e.preventDefault();
    }
    $(document).on("dragenter", stopDefault);
    $(document).on("dragexit", stopDefault);
    $(document).on("dragleave", stopDefault);
    $(document).on("dragover", stopDefault);
    $(document).on("drop", stopDefault);
}
