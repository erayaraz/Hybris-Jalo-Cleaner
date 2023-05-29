# Get the current script's directory
$currentScriptDirectory = Split-Path -Parent $MyInvocation.MyCommand.Path
$parentCurrentScriptDirectory =  Split-Path -Parent $currentScriptDirectory

# Get the current date and time
$currentDateTime = Get-Date -Format "dd-MM-yyyy-hh-tt"

# Log folder
$logFolder = Join-Path -Path $currentScriptDirectory -ChildPath "log"

# Create the log folder if it doesn't exist
if (-not (Test-Path $logFolder)) {
    New-Item -ItemType Directory -Path $logFolder | Out-Null
}

# Log file path
$logFilePath = Join-Path -Path $logFolder -ChildPath "logfiles-$currentDateTime.log"

# Exclude file path
$excludeFilePath = Join-Path -Path $currentScriptDirectory -ChildPath "exclude.txt"

# Read exclude class names from file
$excludeClassNames = Get-Content -Path $excludeFilePath

# Main folder
$mainFolder = $parentCurrentScriptDirectory

# File extension
$fileExtensions = @(".class", ".java")

# Function: Delete Jalo classes
function DeleteJaloClasses($folder) {
    $subFolders = Get-ChildItem -Path $folder -Directory
    foreach ($subFolder in $subFolders) {
        if ($subFolder.Name -eq "jalo") {
            $message = "Jalo folder found: $($subFolder.FullName)"
            $message | Out-File -FilePath $logFilePath -Append
            Write-Host $message
            $files = Get-ChildItem -Path $subFolder.FullName -File | Where-Object { $fileExtensions -contains $_.Extension }
            foreach ($file in $files) {
                $fileName = $file.Name
                if ($excludeClassNames -contains $fileName) {
                    $message = "Excluded Jalo class found: $fileName"
                    $message | Out-File -FilePath $logFilePath -Append
                    Write-Host $message
                } else {
                    $message = "Deleting Jalo class: $($file.FullName)"
                    $message | Out-File -FilePath $logFilePath -Append
                    Write-Host $message
                    Remove-Item -Path $file.FullName -Force
                }
            }
        } else {
            DeleteJaloClasses $subFolder.FullName
        }
    }
}

# Save start time
$startTime = Get-Date

# Delete Jalo classes
DeleteJaloClasses $mainFolder

# Save end time
$endTime = Get-Date

# Calculate total time
$duration = $endTime - $startTime

$message = "All Jalo classes successfully deleted. Total time: $duration seconds"
$message | Out-File -FilePath $logFilePath -Append
Write-Host $message
