package com.example.demo;

import org.junit.Test;
import java.util.Map;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertTrue;

public class AppTest {

    @Test
    public void testToJson() throws Exception {
        App app = new App();
        String json = app.toJson();
        assertTrue("JSON should contain the app name", json.contains("demo"));
    }

    @Test
    public void testLoadYaml() {
        App app = new App();
        Map<String, Object> config = app.loadYaml();
        assertEquals("demo", config.get("app"));
        assertEquals(true, config.get("enabled"));
    }
}
