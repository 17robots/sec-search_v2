# default = docker run imgname:imgver -it volmount volmount python __main__.py search    

param (
    [Alias('c')]
    [Parameter()]
    [string] $command = 'search',

    [Alias('h')]
    [Parameter()]
    [switch] $help,

    [Alias('b')]
    [Parameter()]
    [switch] $build,

    [Alias('p')]
    [Parameter()]
    [switch] $pull,

    [Parameter()] [string] $ssopath = "$($env:USERPROFILE)\.aws\",
    [Parameter()] [string] $output = $PSScriptRoot
)


$IMG_NAME = 'awssearch'
$IMG_VER = '0.0.1'
$REPO_LOC = 'https://github.com/17robots/sec-search_v2.git'

$hello = @"
    [Parameter] command, -c the subcommand and options to run with the script
    [Parameter] help, -h show this help message
    [Parameter] build, -b build the image from source
    [Parameter] pull, -p pulls the image from the specific tag
    [Parameter] ssopath, -s the path to the sso cache folder
    [Parameter] output, -o the path to the output folder
    
    [Example]
    .\awstool.ps1 -c 'search -ports="80,8080" -output="c:\temp\output.txt"'
"@

function build() {
    git clone $($REPO_LOC) build
    cd ./build
    docker build -t "$($IMG_NAME):$($IMG_VER)" .
    cd ..
}

function pull() {
    docker pull "$($IMG_NAME):$($IMG_VER)",
    if((docker image list | Select-String "$($IMG_NAME)").Length -eq 0) {
        throw "Image not found"
    }
}

function run() {
    Invoke-Command -ScriptBlock {
        docker run -v "$($ssopath):/usr/src/user/.aws" -v "$($output):/usr/src/app/output" -it  --rm -t "$($IMG_NAME):$($IMG_VER)" "python" "__main__.py" $($command).Split(' ')
    }
}

if($help) {
    Write-Host $hello
    return
}

if($build) {
    Write-Host "Building image"
    build
    return
}

if($pull) {
    try {
        Write-Host "Pulling image..."
        pull
    } catch {
        Write-Host "Could not pull image"
    }
    return
}

$tokenTime = (Get-Date).AddHours(-12)
if((Test-Path "$($ssopath)\sso\cache") -ne $true -or (Get-ChildItem -Path "$($ssopath)\sso\cache" | Where-Object { $_.CreationTime -ge ($tokenTime).Date}).Length -eq 0) {
    aws sso login --profile AWSPowerUserAccess
}

try {
    pull
} catch {
    Write-Host "Could not pull image"
    build
}

run
