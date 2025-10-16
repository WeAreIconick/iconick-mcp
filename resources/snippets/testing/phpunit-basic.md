# PHPUnit Test Examples

```php
<?php
class Test_My_Plugin extends WP_UnitTestCase {
    
    function test_plugin_activated() {
        $this->assertTrue( is_plugin_active( 'my-plugin/my-plugin.php' ) );
    }
    
    function test_post_creation() {
        $post_id = $this->factory()->post->create( array(
            'post_title' => 'Test Post',
            'post_status' => 'publish'
        ));
        
        $this->assertGreaterThan( 0, $post_id );
        
        $post = get_post( $post_id );
        $this->assertEquals( 'Test Post', $post->post_title );
    }
    
    function test_custom_function() {
        $result = my_custom_function( 'input' );
        $this->assertEquals( 'expected_output', $result );
    }
    
    function test_meta_update() {
        $post_id = $this->factory()->post->create();
        
        update_post_meta( $post_id, '_test_meta', 'test_value' );
        
        $value = get_post_meta( $post_id, '_test_meta', true );
        $this->assertEquals( 'test_value', $value );
    }
    
    function test_user_capabilities() {
        $user_id = $this->factory()->user->create( array( 'role' => 'editor' ) );
        $user = get_user_by( 'id', $user_id );
        
        $this->assertTrue( user_can( $user, 'edit_posts' ) );
        $this->assertFalse( user_can( $user, 'manage_options' ) );
    }
    
    function test_rest_endpoint() {
        $request = new WP_REST_Request( 'GET', '/myplugin/v1/items' );
        $response = rest_do_request( $request );
        
        $this->assertEquals( 200, $response->get_status() );
        $this->assertIsArray( $response->get_data() );
    }
}
```
