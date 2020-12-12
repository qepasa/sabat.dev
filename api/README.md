# sabat.dev api

## https://sabat.dev/api/

## Api Version: 1.1

### Overview

This is the official [sabat.dev](https://sabat.dev) api documentation. This api will always remain open and will not require stupid auth keys.  
It mostly consists of RESTful endpoints that i use for my personal / school projects.

## Timetable

##### Overview
Get the timetable of `class` for this week.

###### URL
    /api/tta

###### URL parameters
- `c` - class identifier (example of id: 3F) **(required)**
- `o` - offset in weeks from the current date **(optional)**
- `dbg` - debug flag **(optional)**

###### Response
A JSON object containing the `resp` list as well as the `success` flag.  

`resp` is an array of length 5, where indicies are mapped to days of the week (mon - 0; fri - 4)  
`resp[n]` is an array of arrays containing `lesson` objects.  
Each `lesson` has its `"classroom", "color", "date", "day_index", "duration", "subject", "teacher","group", "time_index"`  

when number of elements in `resp[n][k]` is greater than one, it indicates that there are multiple lessons happening at once.
```json
{
    "success": true,
    "resp": [
        [[{...}],[{...},{...}]],
        [[{...}],[{...}]],
        [[{...}]],
        [[{...}]],
        [[{...}],[{...}],[{...}]]
    ]
}
```

## Substitutions

##### Overview
Get the timetable of `class` for this week.

###### URL
    /api/sub
###### URL parameters
- `c` - class identifier (example of id: 3F) **(required)**
- `o` - offset in days from the current date **(optional)**
- `dbg` - debug flag **(optional)**

###### Response
A JSON object containing the `resp` list as well as the `success` flag.  

`resp` is an array of arrays, where `resp[n][0]` is the time index and `resp[n][1]` is the included status / message.  
###### Note
The changes are already included in the `/api/tta` endpoint and their only purpose is to be printed out in its native format e.g. `"${resp[n][0]}, ${resp[n][1]}"`.

```json
{
	"success": true,
	"resp": [
		[
			"(0)","Religia - Anulowano"
		]
	]
}
```  

## Class list

##### Overview
Get a list of class identifiers.

###### URL
    /api/cla

###### Response
A JSON object containing the `resp` list as well as the `success` flag.  
`resp` is an array of strings representing the individual class id.  

```json
{
    "success": true,
    "resp": [
        "1A","1B","1C",...,"2Bg","2Cg",...,"3D","3F","3G"
    ]
}
```
