<?php
if(!function_exists('wp_get_current_user')) {
    include(ABSPATH . "wp-includes/pluggable.php"); 
}  

if ( is_user_logged_in() ) {
	$current_user = wp_get_current_user();
	echo $current_user;
} else {
	echo 'Flase';
}

?>