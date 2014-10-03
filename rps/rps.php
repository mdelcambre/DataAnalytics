<?php


$plays = array('rock','paper','scissors');

$throw = $_POST['throw'];
$req_uuid = $_POST['uuid'];
$req_name = base64_encode($_POST['name']);
$previous = false;
$ctime = time();

if (file_exists('play.txt')){
	if (filemtime('play.txt') + 10 < $ctime){
		unlink('play.txt');
		break;
	}
	$previous = true;
	$lines = file('play.txt');
	list($ptime,$uuid,$name,$play) = preg_split('/[\s]/',$lines[0]);
}

if ($previous){
	if($uuid != $req_uuid){
		$play_file = fopen('play.txt','w');
		fwrite($play_file, "$ctime $req_uuid $req_name $throw");
		fclose($play_file);
		$response = array( 'wait'=>false,
				   'name'=>base64_decode($name),
                                   'throw'=>$play);
		echo json_encode($response);
	} elseif($ctime> $ptime+2){
		unlink('play.txt');
		$response = array( 'wait'=>false,
				   'name'=>'Computer',
                                   'throw'=>$plays[array_rand($plays)]);
		echo json_encode($response);
	} else {
		$response = array( 'wait'=>true);
		echo json_encode($response);
	}
} else {		
	$play_file = fopen('play.txt','w');
	fwrite($play_file, "$ctime $req_uuid $req_name $throw");
	fclose($play_file);
	$response = array( 'wait'=>true);
	echo json_encode($response);
}
?>		
