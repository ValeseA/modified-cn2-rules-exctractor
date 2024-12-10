import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart' show rootBundle;
import 'package:audioplayers/audioplayers.dart';

// Variables for genre selection
dynamic selectedGenre1 = "blues";
dynamic selectedGenre2 = "classical";

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});
  
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Nervous',
      home: Scaffold(
        appBar: AppBar(
          title: const Text('Nervous 6.2.10'),
        ),
        body: const MainWidget(),
      ),
    );
  }
}

// Function to parse the JSON data based on the selected genres
Future<String> parseData() async {
  String path = 'assets/' + selectedGenre1 + '_' + selectedGenre2 + '.json';
  final String jsonData = await rootBundle.loadString(path);
  return jsonData;
}

class MainWidget extends StatefulWidget {
  const MainWidget({Key? key}) : super(key: key);

  @override
  State<MainWidget> createState() => _MainWidgetState();
}

class _MainWidgetState extends State<MainWidget> {
  
  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        const SizedBox(height: 10),
        Container(
          child: Wrap(
            spacing: 100,
            children: [
              const GenreSelector1(),
              const GenreSelector2(),
              ClipRRect(
                borderRadius: BorderRadius.circular(4),
                child: Stack(
                  children: <Widget>[
                    Positioned.fill(
                      child: Container(
                        decoration: const BoxDecoration(
                          gradient: LinearGradient(
                            colors: <Color>[
                              Color(0xFF0D47A1),
                              Color(0xFF1976D2),
                              Color(0xFF42A5F5),
                            ],
                          ),
                        ),
                      ),
                    ),
                    TextButton(
                      style: TextButton.styleFrom(
                        foregroundColor: Colors.white, 
                        padding: const EdgeInsets.all(16.0),
                        textStyle: const TextStyle(fontSize: 20),
                      ),
                      onPressed: () {
                        setState(() {
                          // Add your functionality here
                        });
                      },
                      child: const Text('Combine!'),
                    ),
                  ],
                ),
              ),
            ],
          ),
        ),
        const Divider(color: Colors.blue),
        const Row(
          children: [
            Wrap(
              children: [
                SizedBox(
                  width: 55.0,
                  height: 42.0,
                  child: Text(
                    "#", 
                    style: TextStyle(fontWeight: FontWeight.bold), 
                    textAlign: TextAlign.center,
                  ),
                ),
                SizedBox(
                  width: 400.0,
                  height: 42.0,
                  child: Text(
                    "Song", 
                    style: TextStyle(fontWeight: FontWeight.bold)
                  ),
                ),
                SizedBox(
                  width: 400.0,
                  height: 42.0,
                  child: Text(
                    "Original Genre", 
                    style: TextStyle(fontWeight: FontWeight.bold)
                  ),
                ),
                SizedBox(
                  width: 800.0,
                  height: 42.0,
                  child: Text(
                    "Listen", 
                    style: TextStyle(fontWeight: FontWeight.bold)
                  ),
                ),
              ],
            ),
          ]
        ),
        Container(child: SongListWidget()),
      ],
    );
  }
}

// Widget to handle audio playback and display song list
Widget SongListWidget() {
  final AudioPlayer _audioPlayer = AudioPlayer();

  // Function to play audio
  void _playAudio(String fileName) async {
    final player = _audioPlayer;
    String audioPath = 'audio/$fileName';  // Path to the audio file
    await player.play(AssetSource(audioPath));
  }

  // Function to stop audio
  void _stopAudio() async {
    try {
      await _audioPlayer.stop(); // Stop audio playback
    } catch (e) {
      print('Error stopping audio: $e');
    }
  }

  return FutureBuilder(
    builder: (context, projectSnap) {
      if (!projectSnap.hasData) {
        return Container();
      }

      dynamic songsData = jsonDecode(projectSnap.data.toString());
      return ListView.builder(
        padding: const EdgeInsets.all(20.0),
        scrollDirection: Axis.vertical,
        shrinkWrap: true,
        itemCount: 10,
        itemBuilder: (BuildContext context, int index) {
          return Column(
            children: [
              const Divider(color: Colors.blue),
              Row(
                children: [
                  Wrap(
                    children: [
                      SizedBox(
                        width: 40.0,
                        height: 42.0,
                        child: Text(
                          (index + 1).toString(), 
                          style: const TextStyle(fontWeight: FontWeight.bold)
                        ),
                      ),
                      SizedBox(
                        width: 400.0,
                        height: 42.0,
                        child: Text(
                          songsData["songs_list"][index]["filename"]
                        ),
                      ),
                      SizedBox(
                        width: 400.0,
                        height: 42.0,
                        child: Text(
                          songsData["songs_list"][index]["label"]
                        ),
                      ),
                      IconButton(
                        onPressed: () {
                          _playAudio(songsData["songs_list"][index]["filename"]);
                        },
                        icon: const Icon(Icons.volume_up),
                      ),
                      IconButton(
                        onPressed: () {
                          _stopAudio();
                        },
                        icon: const Icon(Icons.stop),
                      ),
                    ]
                  ),
                ],
              ),
            ],
          );
        });
    },
    future: parseData(),
  );
}

// Dropdown menu for selecting the first genre
class GenreSelector1 extends StatefulWidget {
  const GenreSelector1({Key? key}) : super(key: key);

  @override
  State<GenreSelector1> createState() => _GenreSelectorState1();
}

class _GenreSelectorState1 extends State<GenreSelector1> {
  String dropdownValue = 'blues';

  @override
  Widget build(BuildContext context) {
    return DropdownButton<String>(
      value: dropdownValue,
      icon: const Icon(Icons.arrow_downward),
      elevation: 16,
      style: const TextStyle(color: Colors.blue),
      underline: Container(
        height: 2,
        color: Colors.blueAccent,
      ),
      onChanged: (String? newValue) {
        selectedGenre1 = newValue;
        setState(() {
          dropdownValue = newValue!;
        });
      },
      items: <String>['blues','classical','country','disco','hiphop','jazz','metal','pop','reggae','rock']
          .map<DropdownMenuItem<String>>((String value) {
        return DropdownMenuItem<String>(
          value: value,
          child: Text(value),
        );
      }).toList(),
    );
  }
}

// Dropdown menu for selecting the second genre
class GenreSelector2 extends StatefulWidget {
  const GenreSelector2({Key? key}) : super(key: key);

  @override
  State<GenreSelector2> createState() => _GenreSelectorState2();
}

class _GenreSelectorState2 extends State<GenreSelector2> {
  String dropdownValue = 'classical';

  @override
  Widget build(BuildContext context) {
    return DropdownButton<String>(
      value: dropdownValue,
      icon: const Icon(Icons.arrow_downward),
      elevation: 16,
      style: const TextStyle(color: Colors.blue),
      underline: Container(
        height: 2,
        color: Colors.blueAccent,
      ),
      onChanged: (String? newValue) {
        selectedGenre2 = newValue;
        setState(() {
          dropdownValue = newValue!;
        });
      },
      items: <String>['blues','classical','country','disco','hiphop','jazz','metal','pop','reggae','rock']
          .map<DropdownMenuItem<String>>((String value) {
        return DropdownMenuItem<String>(
          value: value,
          child: Text(value),
        );
      }).toList(),
    );
  }
}
