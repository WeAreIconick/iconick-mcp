# WordPress Filesystem API

The Filesystem API provides secure file operations that work across different hosting configurations.

## Basic Usage

### Initialize Filesystem

```php
// Initialize WordPress filesystem
function init_wp_filesystem() {
    global $wp_filesystem;
    
    if ( empty( $wp_filesystem ) ) {
        require_once ABSPATH . '/wp-admin/includes/file.php';
        WP_Filesystem();
    }
    
    return $wp_filesystem;
}

// Check if filesystem is available
function is_filesystem_available() {
    global $wp_filesystem;
    return $wp_filesystem && method_exists( $wp_filesystem, 'put_contents' );
}
```

### Reading Files

```php
function read_file_content( $file_path ) {
    global $wp_filesystem;
    
    if ( ! init_wp_filesystem() ) {
        return false;
    }
    
    // Check if file exists
    if ( ! $wp_filesystem->exists( $file_path ) ) {
        return false;
    }
    
    // Read file content
    $content = $wp_filesystem->get_contents( $file_path );
    
    if ( $content === false ) {
        return false;
    }
    
    return $content;
}

// Usage
$config_content = read_file_content( ABSPATH . 'wp-config.php' );
```

### Writing Files

```php
function write_file_content( $file_path, $content ) {
    global $wp_filesystem;
    
    if ( ! init_wp_filesystem() ) {
        return false;
    }
    
    // Create directory if it doesn't exist
    $dir = dirname( $file_path );
    if ( ! $wp_filesystem->exists( $dir ) ) {
        if ( ! $wp_filesystem->mkdir( $dir, FS_CHMOD_DIR ) ) {
            return false;
        }
    }
    
    // Write file content
    $result = $wp_filesystem->put_contents( 
        $file_path, 
        $content, 
        FS_CHMOD_FILE 
    );
    
    return $result !== false;
}

// Usage
$log_content = "Error occurred at " . current_time( 'mysql' ) . "\n";
write_file_content( WP_CONTENT_DIR . '/debug.log', $log_content );
```

## Advanced File Operations

### Directory Operations

```php
function create_plugin_directory( $plugin_slug ) {
    global $wp_filesystem;
    
    if ( ! init_wp_filesystem() ) {
        return false;
    }
    
    $plugin_dir = WP_CONTENT_DIR . '/uploads/' . $plugin_slug;
    
    // Check if directory exists
    if ( $wp_filesystem->exists( $plugin_dir ) ) {
        return $plugin_dir;
    }
    
    // Create directory
    if ( $wp_filesystem->mkdir( $plugin_dir, FS_CHMOD_DIR ) ) {
        return $plugin_dir;
    }
    
    return false;
}

function list_directory_contents( $directory ) {
    global $wp_filesystem;
    
    if ( ! init_wp_filesystem() ) {
        return false;
    }
    
    if ( ! $wp_filesystem->exists( $directory ) ) {
        return false;
    }
    
    return $wp_filesystem->dirlist( $directory );
}

// Usage
$upload_dir = create_plugin_directory( 'my-plugin' );
if ( $upload_dir ) {
    $contents = list_directory_contents( $upload_dir );
}
```

### File Permissions and Ownership

```php
function set_file_permissions( $file_path, $permissions = FS_CHMOD_FILE ) {
    global $wp_filesystem;
    
    if ( ! init_wp_filesystem() ) {
        return false;
    }
    
    return $wp_filesystem->chmod( $file_path, $permissions );
}

function get_file_info( $file_path ) {
    global $wp_filesystem;
    
    if ( ! init_wp_filesystem() ) {
        return false;
    }
    
    if ( ! $wp_filesystem->exists( $file_path ) ) {
        return false;
    }
    
    return array(
        'exists' => true,
        'size' => $wp_filesystem->size( $file_path ),
        'modified' => $wp_filesystem->mtime( $file_path ),
        'permissions' => $wp_filesystem->getchmod( $file_path )
    );
}
```

## File Upload Handling

### Secure File Upload

```php
function handle_secure_upload( $file, $allowed_types = array() ) {
    // Validate file
    if ( ! $file || ! isset( $file['tmp_name'] ) || ! is_uploaded_file( $file['tmp_name'] ) ) {
        return false;
    }
    
    // Check file size
    $max_size = 5 * 1024 * 1024; // 5MB
    if ( $file['size'] > $max_size ) {
        return false;
    }
    
    // Validate file type
    $file_type = wp_check_filetype( $file['name'] );
    if ( ! empty( $allowed_types ) && ! in_array( $file_type['type'], $allowed_types ) ) {
        return false;
    }
    
    // Generate secure filename
    $filename = sanitize_file_name( $file['name'] );
    $filename = wp_unique_filename( WP_CONTENT_DIR . '/uploads/', $filename );
    
    // Move file using filesystem API
    global $wp_filesystem;
    if ( ! init_wp_filesystem() ) {
        return false;
    }
    
    $upload_path = WP_CONTENT_DIR . '/uploads/' . $filename;
    
    if ( $wp_filesystem->move( $file['tmp_name'], $upload_path ) ) {
        return array(
            'success' => true,
            'filename' => $filename,
            'path' => $upload_path,
            'url' => content_url( 'uploads/' . $filename )
        );
    }
    
    return false;
}

// Usage
if ( isset( $_FILES['custom_upload'] ) ) {
    $allowed_types = array( 'image/jpeg', 'image/png', 'application/pdf' );
    $result = handle_secure_upload( $_FILES['custom_upload'], $allowed_types );
    
    if ( $result && $result['success'] ) {
        echo 'File uploaded successfully: ' . $result['url'];
    } else {
        echo 'Upload failed';
    }
}
```

### Image Processing

```php
function process_uploaded_image( $file_path, $max_width = 800, $max_height = 600 ) {
    // Check if file is an image
    $image_info = getimagesize( $file_path );
    if ( $image_info === false ) {
        return false;
    }
    
    $width = $image_info[0];
    $height = $image_info[1];
    
    // Check if resizing is needed
    if ( $width <= $max_width && $height <= $max_height ) {
        return $file_path; // No resizing needed
    }
    
    // Calculate new dimensions
    $ratio = min( $max_width / $width, $max_height / $height );
    $new_width = intval( $width * $ratio );
    $new_height = intval( $height * $ratio );
    
    // Create image resource based on type
    $image_type = $image_info[2];
    switch ( $image_type ) {
        case IMAGETYPE_JPEG:
            $source = imagecreatefromjpeg( $file_path );
            break;
        case IMAGETYPE_PNG:
            $source = imagecreatefrompng( $file_path );
            break;
        case IMAGETYPE_GIF:
            $source = imagecreatefromgif( $file_path );
            break;
        default:
            return false;
    }
    
    if ( ! $source ) {
        return false;
    }
    
    // Create new image
    $resized = imagecreatetruecolor( $new_width, $new_height );
    
    // Preserve transparency for PNG and GIF
    if ( $image_type == IMAGETYPE_PNG || $image_type == IMAGETYPE_GIF ) {
        imagealphablending( $resized, false );
        imagesavealpha( $resized, true );
        $transparent = imagecolorallocatealpha( $resized, 255, 255, 255, 127 );
        imagefilledrectangle( $resized, 0, 0, $new_width, $new_height, $transparent );
    }
    
    // Resize image
    imagecopyresampled( 
        $resized, $source, 
        0, 0, 0, 0, 
        $new_width, $new_height, 
        $width, $height 
    );
    
    // Save resized image
    $resized_path = str_replace( '.', '_resized.', $file_path );
    
    switch ( $image_type ) {
        case IMAGETYPE_JPEG:
            imagejpeg( $resized, $resized_path, 90 );
            break;
        case IMAGETYPE_PNG:
            imagepng( $resized, $resized_path, 9 );
            break;
        case IMAGETYPE_GIF:
            imagegif( $resized, $resized_path );
            break;
    }
    
    // Clean up
    imagedestroy( $source );
    imagedestroy( $resized );
    
    return $resized_path;
}
```

## Configuration File Management

### Reading Configuration Files

```php
function read_config_file( $config_path ) {
    global $wp_filesystem;
    
    if ( ! init_wp_filesystem() ) {
        return false;
    }
    
    if ( ! $wp_filesystem->exists( $config_path ) ) {
        return false;
    }
    
    $content = $wp_filesystem->get_contents( $config_path );
    
    if ( $content === false ) {
        return false;
    }
    
    // Parse configuration
    $config = array();
    $lines = explode( "\n", $content );
    
    foreach ( $lines as $line ) {
        $line = trim( $line );
        
        // Skip empty lines and comments
        if ( empty( $line ) || strpos( $line, '#' ) === 0 ) {
            continue;
        }
        
        // Parse key=value pairs
        if ( strpos( $line, '=' ) !== false ) {
            list( $key, $value ) = explode( '=', $line, 2 );
            $config[ trim( $key ) ] = trim( $value );
        }
    }
    
    return $config;
}
```

### Writing Configuration Files

```php
function write_config_file( $config_path, $config_data ) {
    global $wp_filesystem;
    
    if ( ! init_wp_filesystem() ) {
        return false;
    }
    
    // Create backup
    if ( $wp_filesystem->exists( $config_path ) ) {
        $backup_path = $config_path . '.backup.' . time();
        $wp_filesystem->copy( $config_path, $backup_path );
    }
    
    // Build config content
    $content = "# Configuration file\n";
    $content .= "# Generated on " . current_time( 'mysql' ) . "\n\n";
    
    foreach ( $config_data as $key => $value ) {
        $content .= $key . ' = ' . $value . "\n";
    }
    
    // Write file
    $result = $wp_filesystem->put_contents( 
        $config_path, 
        $content, 
        FS_CHMOD_FILE 
    );
    
    return $result !== false;
}
```

## Log File Management

### Secure Logging

```php
function write_log_entry( $message, $log_file = 'custom.log' ) {
    global $wp_filesystem;
    
    if ( ! init_wp_filesystem() ) {
        return false;
    }
    
    $log_dir = WP_CONTENT_DIR . '/logs/';
    $log_path = $log_dir . $log_file;
    
    // Create log directory if it doesn't exist
    if ( ! $wp_filesystem->exists( $log_dir ) ) {
        $wp_filesystem->mkdir( $log_dir, FS_CHMOD_DIR );
    }
    
    // Sanitize message
    $message = sanitize_text_field( $message );
    
    // Format log entry
    $log_entry = sprintf( 
        "[%s] %s\n", 
        current_time( 'Y-m-d H:i:s' ), 
        $message 
    );
    
    // Append to log file
    $current_content = '';
    if ( $wp_filesystem->exists( $log_path ) ) {
        $current_content = $wp_filesystem->get_contents( $log_path );
    }
    
    $new_content = $current_content . $log_entry;
    
    return $wp_filesystem->put_contents( 
        $log_path, 
        $new_content, 
        FS_CHMOD_FILE 
    ) !== false;
}

function clean_old_logs( $log_dir, $max_age_days = 30 ) {
    global $wp_filesystem;
    
    if ( ! init_wp_filesystem() ) {
        return false;
    }
    
    if ( ! $wp_filesystem->exists( $log_dir ) ) {
        return true;
    }
    
    $files = $wp_filesystem->dirlist( $log_dir );
    $cutoff_time = time() - ( $max_age_days * 24 * 60 * 60 );
    
    foreach ( $files as $file ) {
        $file_path = $log_dir . '/' . $file['name'];
        
        if ( $file['lastmodunix'] < $cutoff_time ) {
            $wp_filesystem->delete( $file_path );
        }
    }
    
    return true;
}
```

## Security Considerations

### File Path Validation

```php
function validate_file_path( $file_path, $allowed_dirs = array() ) {
    // Resolve real path
    $real_path = realpath( $file_path );
    
    if ( $real_path === false ) {
        return false;
    }
    
    // Check if path is within allowed directories
    if ( ! empty( $allowed_dirs ) ) {
        $allowed = false;
        
        foreach ( $allowed_dirs as $allowed_dir ) {
            $allowed_dir = realpath( $allowed_dir );
            
            if ( $allowed_dir !== false && strpos( $real_path, $allowed_dir ) === 0 ) {
                $allowed = true;
                break;
            }
        }
        
        if ( ! $allowed ) {
            return false;
        }
    }
    
    // Prevent directory traversal
    if ( strpos( $file_path, '..' ) !== false ) {
        return false;
    }
    
    return true;
}

function secure_file_operation( $operation, $file_path, $data = null ) {
    // Allowed directories
    $allowed_dirs = array(
        WP_CONTENT_DIR . '/uploads/',
        WP_CONTENT_DIR . '/logs/',
        WP_CONTENT_DIR . '/cache/'
    );
    
    // Validate file path
    if ( ! validate_file_path( $file_path, $allowed_dirs ) ) {
        return false;
    }
    
    // Sanitize file path
    $file_path = sanitize_file_name( $file_path );
    
    global $wp_filesystem;
    if ( ! init_wp_filesystem() ) {
        return false;
    }
    
    // Perform operation
    switch ( $operation ) {
        case 'read':
            return $wp_filesystem->get_contents( $file_path );
        case 'write':
            return $wp_filesystem->put_contents( $file_path, $data, FS_CHMOD_FILE );
        case 'delete':
            return $wp_filesystem->delete( $file_path );
        case 'exists':
            return $wp_filesystem->exists( $file_path );
        default:
            return false;
    }
}
```

## Best Practices

### Error Handling

```php
function safe_file_operation( $callback ) {
    global $wp_filesystem;
    
    try {
        if ( ! init_wp_filesystem() ) {
            throw new Exception( 'Failed to initialize filesystem' );
        }
        
        return $callback( $wp_filesystem );
        
    } catch ( Exception $e ) {
        error_log( 'Filesystem operation failed: ' . $e->getMessage() );
        return false;
    }
}

// Usage
$result = safe_file_operation( function( $wp_filesystem ) {
    return $wp_filesystem->put_contents( 
        WP_CONTENT_DIR . '/uploads/test.txt', 
        'Hello World', 
        FS_CHMOD_FILE 
    );
} );
```

### Performance Optimization

```php
function batch_file_operations( $operations ) {
    global $wp_filesystem;
    
    if ( ! init_wp_filesystem() ) {
        return false;
    }
    
    $results = array();
    
    foreach ( $operations as $operation ) {
        $type = $operation['type'];
        $path = $operation['path'];
        $data = $operation['data'] ?? null;
        
        switch ( $type ) {
            case 'write':
                $results[] = $wp_filesystem->put_contents( $path, $data, FS_CHMOD_FILE );
                break;
            case 'delete':
                $results[] = $wp_filesystem->delete( $path );
                break;
            case 'mkdir':
                $results[] = $wp_filesystem->mkdir( $path, FS_CHMOD_DIR );
                break;
            default:
                $results[] = false;
        }
    }
    
    return $results;
}
```

## Official Documentation

https://developer.wordpress.org/apis/filesystem/
https://developer.wordpress.org/reference/classes/wp_filesystem/
https://developer.wordpress.org/reference/functions/wp_filesystem/
